import argparse
import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from imutils import paths
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras.callbacks import (
    EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
)
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical

from pocovidnet.model import get_dense_model
from pocovidnet.utils import Metrics

# Suppress logging
tf.get_logger().setLevel('ERROR')

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    '-d', '--data_dir', required=True, help='path to input dataset'
)
ap.add_argument('-m', '--model_dir', type=str, default='models/')
ap.add_argument(
    '-f', '--fold', type=int, default='0', help='fold to take as test data'
)
ap.add_argument('-gl', '--global_average_pooling', action='store_true')
ap.add_argument('-lr', '--learning_rate', type=float, default=1e-4)
ap.add_argument('-ep', '--epochs', type=int, default=20)
ap.add_argument('-bs', '--batch_size', type=int, default=16)
ap.add_argument('-bn', '--batch_norm', type=bool, default=True)
ap.add_argument('-dr', '--dropout', type=float, default=0.3)
ap.add_argument('-iw', '--img_width', type=int, default=7)
ap.add_argument('-ih', '--img_height', type=int, default=9)
ap.add_argument('-ls', '--log_softmax', action='store_true')
ap.add_argument('-n', '--model_name', type=str, default='test')
ap.add_argument('-hs', '--hidden_size', type=str, default="[512, 256]")
ap.add_argument('-feat', '--features', type=int, default=1)

args = vars(ap.parse_args())
# Initialize hyperparameters
DATA_DIR = args['data_dir']
MODEL_NAME = args['model_name']
FOLD = args['fold']
MODEL_DIR = os.path.join(args['model_dir'], MODEL_NAME, f'fold_{FOLD}')
LR = args['learning_rate']
EPOCHS = args['epochs']
BATCH_SIZE = args['batch_size']
IMG_WIDTH, IMG_HEIGHT = args['img_width'], args['img_height']
LOG_SOFTMAX = args['log_softmax']
HIDDEN_SIZES = eval(args['hidden_size'])
FEAT_ID = args['features']
POOLING = args['global_average_pooling']
BATCH_NORM = args['batch_norm']
DROPOUT = args['dropout']

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)
print(f'Model parameters: {args}')
# grab the list of images in our dataset directory, then initialize
# the list of data (i.e., images) and class images
print('Loading images...')
imagePaths = list(paths.list_files(DATA_DIR))
data = []
labels = []

print(f'selected fold: {FOLD}')

train_labels, test_labels = [], []
train_data, test_data = [], []
# test_files = []

# loop over folds
for imagePath in imagePaths:
    if not imagePath.endswith('npz'):
        continue

    path_parts = imagePath.split(os.path.sep)
    # extract the split
    train_test = path_parts[-3][-1]
    # extract the class label from the filename
    label = path_parts[-2]
    # load the image, swap color channels, and resize it to be a fixed
    # 224x224 pixels while ignoring aspect ratio
    data = np.load(imagePath)

    if FEAT_ID > 0 and FEAT_ID < 4:
        feats = [FEAT_ID]
    elif type(FEAT_ID) != int:
        raise TypeError('Give int as feature type')
    else:
        feats = [1, 2, 3]

    sample = []
    for feat in feats:
        # Use individual features
        image = cv2.resize(
            data['f' + str(feat)][0, :, :, :], (IMG_WIDTH, IMG_HEIGHT)
        )
        sp = np.mean(image, axis=(0, 1)) if POOLING else image.flatten()
        sample.append(sp)
    sample = np.concatenate(sample).flatten()

    # update the data and labels lists, respectively
    if train_test == str(FOLD):
        test_labels.append(label)
        test_data.append(sample)
        # test_files.append(path_parts[-1])
    else:
        train_labels.append(label)
        train_data.append(sample)

# Prepare data for model
print(
    f'\nNumber of training samples: {len(train_labels)} \n'
    f'Number of testing samples: {len(test_labels)}'
)

assert len(set(train_labels)) == len(set(test_labels)), (
    'Something went wrong. Some classes are only in train or test data.'
)  # yapf: disable

# convert the data and labels to NumPy arrays while scaling the pixel
# intensities to the range [0, 255]
# train_data = np.array(train_data) / 255.0
# test_data = np.array(test_data) / 255.0
train_labels_text = np.array(train_labels)
test_labels_text = np.array(test_labels)

num_classes = len(set(train_labels))

# perform one-hot encoding on the labels
lb = LabelBinarizer()
lb.fit(train_labels_text)

train_labels = lb.transform(train_labels_text)
test_labels = lb.transform(test_labels_text)

if num_classes == 2:
    train_labels = to_categorical(train_labels, num_classes=num_classes)
    test_labels = to_categorical(test_labels, num_classes=num_classes)

trainX = np.stack(train_data)
trainY = np.stack(train_labels)
testX = np.stack(test_data)
testY = np.stack(test_labels)
print('Class mappings are:', lb.classes_)

print(trainX.shape, trainY.shape, testX.shape, testY.shape)

# initialize the training data augmentation object
# trainAug = ImageDataGenerator(
#     rotation_range=10,
#     fill_mode='nearest',
#     horizontal_flip=True,
#     vertical_flip=True,
#     width_shift_range=0.1,
#     height_shift_range=0.1
# )

# Load the VGG16 network
model = get_dense_model(
    input_size=trainX.shape[1],
    num_classes=num_classes,
    dropout=DROPOUT,
    log_softmax=LOG_SOFTMAX,
    batch_norm=BATCH_NORM,
    hidden_sizes=HIDDEN_SIZES,
)

# Define callbacks
earlyStopping = EarlyStopping(
    monitor='val_loss',
    patience=20,
    verbose=1,
    mode='min',
    restore_best_weights=True
)

mcp_save = ModelCheckpoint(
    os.path.join(MODEL_DIR, 'best_weights'),
    save_best_only=True,
    monitor='val_accuracy',
    mode='max',
    verbose=1
)
reduce_lr_loss = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.1,
    patience=7,
    verbose=1,
    epsilon=1e-4,
    mode='min'
)
# To show balanced accuracy
metrics = Metrics((testX, testY), model)

# compile model
print('Compiling model...')
opt = Adam(lr=LR, decay=LR / EPOCHS)
loss = (
    tf.keras.losses.CategoricalCrossentropy() if not LOG_SOFTMAX else (
        lambda labels, targets: tf.reduce_mean(
            tf.reduce_sum(
                -1 * tf.math.multiply(tf.cast(labels, tf.float32), targets),
                axis=1
            )
        )
    )
)

model.compile(loss=loss, optimizer=opt, metrics=['accuracy'])

print(f'Model has {model.count_params()} parameters')
print(f'Model summary {model.summary()}')

# train the head of the network
print('Starting training model...')
H = model.fit(
    trainX,
    trainY,
    steps_per_epoch=len(trainX) // BATCH_SIZE,
    validation_data=(testX, testY),
    validation_steps=len(testX) // BATCH_SIZE,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    callbacks=[earlyStopping, mcp_save, reduce_lr_loss, metrics]
)

# make predictions on the testing set
print('Evaluating network...')
predIdxs = model.predict(testX, batch_size=BATCH_SIZE)

# CSV: save predictions for inspection:
df = pd.DataFrame(predIdxs)
df.to_csv(os.path.join(MODEL_DIR, "_preds_last_epoch.csv"))

# for each image in the testing set we need to find the index of the
# label with corresponding largest predicted probability
predIdxs = np.argmax(predIdxs, axis=1)

print('classification report sklearn:')
print(
    classification_report(
        testY.argmax(axis=1), predIdxs, target_names=lb.classes_
    )
)

# compute the confusion matrix and and use it to derive the raw
# accuracy, sensitivity, and specificity
print('confusion matrix:')
cm = confusion_matrix(testY.argmax(axis=1), predIdxs)
# show the confusion matrix, accuracy, sensitivity, and specificity
print(cm)

# serialize the model to disk
print(f'Saving COVID-19 detector model on {MODEL_DIR} data...')
model.save(os.path.join(MODEL_DIR, 'last_epoch'), save_format='h5')

# plot the training loss and accuracy
N = EPOCHS
plt.style.use('ggplot')
plt.figure()
plt.plot(np.arange(0, N), H.history['loss'], label='train_loss')
plt.plot(np.arange(0, N), H.history['val_loss'], label='val_loss')
plt.plot(np.arange(0, N), H.history['accuracy'], label='train_acc')
plt.plot(np.arange(0, N), H.history['val_accuracy'], label='val_acc')
plt.title('Training Loss and Accuracy on COVID-19 Dataset')
plt.xlabel('Epoch #')
plt.ylabel('Loss/Accuracy')
plt.legend(loc='lower left')
plt.savefig(os.path.join(MODEL_DIR, 'loss.png'))

print('Done, shuttting down!')
