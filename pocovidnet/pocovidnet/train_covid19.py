import argparse
import os

import cv2
import matplotlib.pyplot as plt
import numpy as np

from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras.applications import VGG16
from sklearn.metrics import balanced_accuracy_score
from tensorflow.keras.layers import (
    AveragePooling2D, Dense, Dropout, Flatten, Input
)
from tensorflow.keras.layers import BatchNormalization, ReLU
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import Callback
from tensorflow.keras.callbacks import (
    EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
)
import tensorflow as tf

from imutils import paths

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-d', '--dataset', required=True, help='path to input dataset')
ap.add_argument(
    '-p',
    '--plot',
    type=str,
    default='plots/plot.png',
    help='path to output loss/accuracy plot'
)
ap.add_argument(
    '-m',
    '--model',
    type=str,
    default='trained_model/covid19.model',
    help='path to output loss/accuracy plot'
)
ap.add_argument(
    '-s', '--split', type=int, default='0', help='split to take as test data'
)
args = vars(ap.parse_args())

split = args['split']
dataset_name = os.path.join('..', 'data', 'pocus', 'cross_validation')
model_name = f'pocus_fold_{split}.model'
plot_path = f'pocus_fold_{split}.png'

# Suppress logging
tf.get_logger().setLevel('ERROR')

# initialize the initial learning rate, number of epochs to train for,
# and batch size
INIT_LR = 1e-4
EPOCHS = 25
BS = 16
TRAINABLE_BASE_LAYERS = 2
IMG_WIDTH = 224
IMG_HEIGHT = 224

# grab the list of images in our dataset directory, then initialize
# the list of data (i.e., images) and class images
print('[INFO] loading images...')
imagePaths = list(paths.list_images(dataset_name))
data = []
labels = []

print(f'Model is called : {model_name}')
print(f'Dataset name : {dataset_name}')

print('selected split:', args['split'])

train_labels, test_labels, test_files = [], [], []
train_data, test_data = [], []

# loop over split0, split1 etc
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
    # TESTING
    # image = (imagePath.split(os.path.sep)[-1]).split('.')[0]

    # update the data and labels lists, respectively
    if train_test == str(args['split']):
        test_labels.append(label)
        test_data.append(image)
        test_files.append(imagePath.split(os.path.sep)[-1])
    else:
        train_labels.append(label)
        train_data.append(image)

# Now prepare for KERAS
print(len(test_labels), len(train_labels))
# convert the data and labels to NumPy arrays while scaling the pixel
# intensities to the range [0, 255]
train_data = np.array(train_data) / 255.0
test_data = np.array(test_data) / 255.0

train_labels_text = np.array(train_labels)
test_labels_text = np.array(test_labels)

assert len(set(train_labels)) == len(set(test_labels)), (
    'Some classes are only in train or test data'
)  # yapf: disable
num_classes = len(set(train_labels))

# perform one-hot encoding on the labels
lb = LabelBinarizer()
lb.fit(train_labels_text)

train_labels = lb.transform(train_labels_text)
test_labels = lb.transform(test_labels_text)

if num_classes == 2:
    train_labels = to_categorical(train_labels, num_classes=num_classes)
    test_labels = to_categorical(test_labels, num_classes=num_classes)

# partition the data into training and testing splits using 80% of
# the data for training and the remaining 20% for testing

trainX = train_data
trainY = train_labels
testX = test_data
testY = test_labels
print('train:', trainX.shape, len(trainY), 'test:', testX.shape, len(testY))
weights = {'covid': 0.3, 'pneumonia': 0.3, 'regular': 1}
class_weights = {i: weights[c] for i, c in enumerate(lb.classes_)}

print('Class mappings:', lb.classes_)
print('Class weights:', class_weights)

# initialize the training data augmentation object
trainAug = ImageDataGenerator(
    rotation_range=10,
    fill_mode='nearest',
    horizontal_flip=True,
    vertical_flip=True,
    width_shift_range=0.1,
    height_shift_range=0.1
)

# load the VGG16 network, ensuring the head FC layer sets are left
# off
# baseModel = VGG16(
#     weights='imagenet',
#     include_top=False,
#     input_tensor=Input(shape=(224, 224, 3))
# )
baseModel = VGG16(
    weights='imagenet',
    include_top=False,
    input_tensor=Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3))
)

# construct the head of the model that will be placed on top of the
# the base model
headModel = baseModel.output
headModel = AveragePooling2D(pool_size=(4, 4))(headModel)
headModel = Flatten(name='flatten')(headModel)
headModel = Dense(64)(headModel)
headModel = BatchNormalization()(headModel)
headModel = ReLU()(headModel)
headModel = Dropout(0.5)(headModel)
headModel = Dense(num_classes, activation='softmax')(headModel)

# place the head FC model on top of the base model (this will become
# the actual model we will train)
model = Model(inputs=baseModel.input, outputs=headModel)

# loop over all layers in the base model and freeze them so they will
# *not* be updated during the first training process
num_layers = len(baseModel.layers)
for ind, layer in enumerate(baseModel.layers):
    if ind < num_layers - TRAINABLE_BASE_LAYERS:
        layer.trainable = False

earlyStopping = EarlyStopping(
    monitor='val_loss',
    patience=20,
    verbose=1,
    mode='min',
    restore_best_weights=True
)

mcp_save = ModelCheckpoint(
    'fold_' + str(split) + '_epoch_{epoch:02d}',
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


class Metrics(Callback):

    def __init__(self, valid_data):
        super(Metrics, self).__init__()
        self.valid_data = valid_data
        self._data = []

    def on_epoch_end(self, epoch, logs=None):
        # if epoch:
        #     for i in range(1):  # len(self.valid_data)):
        x_test_batch, y_test_batch = self.valid_data

        y_predict = np.asarray(model.predict(x_test_batch))

        y_val = np.argmax(y_test_batch, axis=1)
        y_predict = np.argmax(y_predict, axis=1)
        self._data.append(
            {
                'val_balanced': balanced_accuracy_score(y_val, y_predict),
            }
        )
        print(self._data[-1])
        return

    def get_data(self):
        return self._data


# compile our model
print('[INFO] compiling model...')
opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
model.compile(
    loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy']
)

print(f'Model has {model.count_params()} parameters')
print(f'Model summary {model.summary()}')

metrics = Metrics((testX, testY))

# train the head of the network
print('[INFO] training head...')
H = model.fit_generator(
    trainAug.flow(trainX, trainY, batch_size=BS),
    steps_per_epoch=len(trainX) // BS,
    validation_data=(testX, testY),
    validation_steps=len(testX) // BS,
    epochs=EPOCHS,
    callbacks=[earlyStopping, mcp_save, reduce_lr_loss, metrics],
    class_weight=class_weights
)

# make predictions on the testing set
print('[INFO] evaluating network...')
predIdxs = model.predict(testX, batch_size=BS)

# for each image in the testing set we need to find the index of the
# label with corresponding largest predicted probability
predIdxs = np.argmax(predIdxs, axis=1)

# print('accuracy sklearn: ', accuracy_score(predIdxs, testY.argmax(axis=1)))

print('classification report sklearn:')
# show a nicely formatted classification report
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
print(f'[INFO] saving COVID-19 detector model on {model_name} data...')
model.save(model_name, save_format='h5')

# print outputs per class
print('check test outputs per file:')
gt = testY.argmax(axis=1)
# print(len(gt), len(predIdxs), len(test_files))
# for i in range(len(predIdxs)):
#     print('gt:', gt[i], 'pred', predIdxs[i], 'filename', test_files[i])

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
plt.savefig(plot_path)
