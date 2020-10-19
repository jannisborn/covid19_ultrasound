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
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical

from pocovidnet import MODEL_FACTORY
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
ap.add_argument('-lr', '--learning_rate', type=float, default=1e-4)
ap.add_argument('-ep', '--epochs', type=int, default=20)
ap.add_argument('-bs', '--batch_size', type=int, default=16)
ap.add_argument('-t', '--trainable_base_layers', type=int, default=1)
ap.add_argument('-iw', '--img_width', type=int, default=224)
ap.add_argument('-ih', '--img_height', type=int, default=224)
ap.add_argument('-id', '--model_id', type=str, default='vgg_base')
ap.add_argument('-ls', '--log_softmax', type=bool, default=False)
ap.add_argument('-n', '--model_name', type=str, default='test')
ap.add_argument('-hs', '--hidden_size', type=int, default=64)
args = vars(ap.parse_args())

# Initialize hyperparameters
DATA_DIR = args['data_dir']
MODEL_NAME = args['model_name']
FOLD = args['fold']
MODEL_DIR = os.path.join(args['model_dir'], MODEL_NAME, f'fold_{FOLD}')
LR = args['learning_rate']
EPOCHS = args['epochs']
BATCH_SIZE = args['batch_size']
MODEL_ID = args['model_id']
TRAINABLE_BASE_LAYERS = args['trainable_base_layers']
IMG_WIDTH, IMG_HEIGHT = args['img_width'], args['img_height']
LOG_SOFTMAX = args['log_softmax']
HIDDEN_SIZE = args['hidden_size']

# Check if model class exists
if MODEL_ID not in MODEL_FACTORY.keys():
    raise ValueError(
        f'Model {MODEL_ID} not implemented. Choose from {MODEL_FACTORY.keys()}'
    )

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)
print(f'Model parameters: {args}')
# grab the list of images in our dataset directory, then initialize
# the list of data (i.e., images) and class images
print('Loading images...')
imagePaths = list(paths.list_images(DATA_DIR))
data = []
labels = []

print(f'selected fold: {FOLD}')

train_labels, test_labels = [], []
train_data, test_data = [], []
# test_files = []

# loop over folds
for imagePath in imagePaths:

    path_parts = imagePath.split(os.path.sep)
    # extract the split
    train_test = path_parts[-3][-1]
    # extract the class label from the filename
    label = path_parts[-2]
    # load the image, swap color channels, and resize it to be a fixed
    # 224x224 pixels while ignoring aspect ratio
    image = cv2.imread(imagePath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))

    # update the data and labels lists, respectively
    if train_test == str(FOLD):
        test_labels.append(label)
        test_data.append(image)
        # test_files.append(path_parts[-1])
    else:
        train_labels.append(label)
        train_data.append(image)

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
train_data = np.array(train_data) / 255.0
test_data = np.array(test_data) / 255.0
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

trainX = train_data
trainY = train_labels
testX = test_data
testY = test_labels
print('Class mappings are:', lb.classes_)

# initialize the training data augmentation object
trainAug = ImageDataGenerator(
    rotation_range=10,
    fill_mode='nearest',
    horizontal_flip=True,
    vertical_flip=True,
    width_shift_range=0.1,
    height_shift_range=0.1
)

# Load the VGG16 network
model = MODEL_FACTORY[MODEL_ID](
    input_size=(IMG_WIDTH, IMG_HEIGHT, 3),
    num_classes=num_classes,
    trainable_layers=TRAINABLE_BASE_LAYERS,
    log_softmax=LOG_SOFTMAX,
    hidden_size=HIDDEN_SIZE
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
    # os.path.join(MODEL_DIR, 'fold_' + str(FOLD) + '_epoch_{epoch:02d}'),
    os.path.join(MODEL_DIR, 'best_weights'),
    save_best_only=True,
    monitor='val_accuracy',
    mode='max',
    verbose=1
)
reduce_lr_loss = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.7,
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
H = model.fit_generator(
    trainAug.flow(trainX, trainY, batch_size=BATCH_SIZE),
    steps_per_epoch=len(trainX) // BATCH_SIZE,
    validation_data=(testX, testY),
    validation_steps=len(testX) // BATCH_SIZE,
    epochs=EPOCHS,
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
