import argparse
import os

import cv2
import matplotlib.pyplot as plt
import numpy as np

from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import (
    AveragePooling2D, Dense, Dropout, Flatten, Input
)
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import (
    EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
)
import tensorflow as tf

from imutils import paths

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True, help="path to input dataset")
ap.add_argument(
    "-p",
    "--plot",
    type=str,
    default="plots/plot.png",
    help="path to output loss/accuracy plot"
)
ap.add_argument(
    "-m",
    "--model",
    type=str,
    default="trained_model/covid19.model",
    help="path to output loss/accuracy plot"
)
args = vars(ap.parse_args())

dataset_name = args['dataset'].split('_')[-1]
model_name = (
    os.path.join('trained_models', dataset_name + '.model')
    if args['model'] == 'trained_model/covid19.model' else args['model']
)
plot_path = (
    os.path.join('plots', dataset_name + '.png')
    if args['plot'] == 'plots/plot.png' else args['plots']  # yapf: disable
)

# Suppress logging
tf.get_logger().setLevel('ERROR')

# initialize the initial learning rate, number of epochs to train for,
# and batch size
INIT_LR = 5e-3
EPOCHS = 50
BS = 8

# grab the list of images in our dataset directory, then initialize
# the list of data (i.e., images) and class images
print("[INFO] loading images...")
imagePaths = list(paths.list_images(args["dataset"]))
data = []
labels = []

print(f"Model is called : {model_name}")
print(f"Dataset name : {dataset_name}")

if dataset_name != 'pocus-splitted':
    # loop over the image paths
    for imagePath in imagePaths:
        # extract the class label from the filename
        label = imagePath.split(os.path.sep)[-2]

        # load the image, swap color channels, and resize it to be a fixed
        # 224x224 pixels while ignoring aspect ratio
        image = cv2.imread(imagePath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (224, 224))

        # update the data and labels lists, respectively
        data.append(image)
        labels.append(label)

    # convert the data and labels to NumPy arrays while scaling the pixel
    # intensities to the range [0, 255]
    data = np.array(data) / 255.0
    labels = np.array(labels)

    # perform one-hot encoding on the labels
    lb = LabelBinarizer()
    num_classes = len(set(labels))

    labels = lb.fit_transform(labels)
    if num_classes == 2:
        labels = to_categorical(labels, num_classes=num_classes)
    # partition the data into training and testing splits using 80% of
    # the data for training and the remaining 20% for testing
    (trainX, testX, trainY, testY) = train_test_split(
        data, labels, test_size=0.20, stratify=labels, random_state=42
    )

    class_weights = {c: 1 for c in range(num_classes)}

else:
    # For the pocus-splitted data
    train_labels, test_labels = [], []
    train_data, test_data = [], []

    # loop over the image paths (train and test)
    for imagePath in imagePaths:

        # extract the class label from the filename
        label = imagePath.split(os.path.sep)[-2]

        # load the image, swap color channels, and resize it to be a fixed
        # 224x224 pixels while ignoring aspect ratio
        image = cv2.imread(imagePath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (224, 224))

        # update the data and labels lists, respectively
        if '/train/' in imagePath:
            train_labels.append(label)
            train_data.append(image)
        elif '/test/' in imagePath:
            test_labels.append(label)
            test_data.append(image)

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
    #weights = {'covid': 0.2, 'pneunomia': 0.3, 'regular': 0.5}
    weights = {'covid': 0.3, 'pneunomia': 0.3, 'regular': 0.3}
    class_weights = {i: weights[c] for i, c in enumerate(lb.classes_)}

print("Class mappings:", lb.classes_)
print("Class weights:", class_weights)
# initialize the training data augmentation object
trainAug = ImageDataGenerator(
    rotation_range=15,
    fill_mode="nearest",
    horizontal_flip=True,
    vertical_flip=True
)

# load the VGG16 network, ensuring the head FC layer sets are left
# off
baseModel = VGG16(
    weights="imagenet",
    include_top=False,
    input_tensor=Input(shape=(224, 224, 3))
)

# construct the head of the model that will be placed on top of the
# the base model
headModel = baseModel.output
headModel = AveragePooling2D(pool_size=(4, 4))(headModel)
headModel = Flatten(name="flatten")(headModel)
headModel = Dense(64, activation="relu")(headModel)
headModel = Dropout(0.5)(headModel)
headModel = Dense(num_classes, activation="softmax")(headModel)

# place the head FC model on top of the base model (this will become
# the actual model we will train)
model = Model(inputs=baseModel.input, outputs=headModel)

# loop over all layers in the base model and freeze them so they will
# *not* be updated during the first training process
for layer in baseModel.layers:
    layer.trainable = False

earlyStopping = EarlyStopping(
    monitor='val_loss', patience=10, verbose=0, mode='min'
)
mcp_save = ModelCheckpoint(
    '.mdl_wts.hdf5', save_best_only=True, monitor='val_loss', mode='min'
)
reduce_lr_loss = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.1,
    patience=7,
    verbose=1,
    epsilon=1e-4,
    mode='min'
)

# compile our model
print("[INFO] compiling model...")
opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])

print(f"Model has {model.count_params()} parameters")
print(f"Model summary {model.summary()}")

# train the head of the network
print("[INFO] training head...")
H = model.fit_generator(
    trainAug.flow(trainX, trainY, batch_size=BS),
    steps_per_epoch=len(trainX) // BS,
    validation_data=(testX, testY),
    validation_steps=len(testX) // BS,
    epochs=EPOCHS,
    class_weight=class_weights,
    callbacks=[earlyStopping, mcp_save, reduce_lr_loss]
)

# make predictions on the testing set
print("[INFO] evaluating network...")
predIdxs = model.predict(testX, batch_size=BS)

# for each image in the testing set we need to find the index of the
# label with corresponding largest predicted probability
predIdxs = np.argmax(predIdxs, axis=1)

# show a nicely formatted classification report
print(
    classification_report(
        testY.argmax(axis=1), predIdxs, target_names=lb.classes_
    )
)

# compute the confusion matrix and and use it to derive the raw
# accuracy, sensitivity, and specificity
cm = confusion_matrix(testY.argmax(axis=1), predIdxs)
total = sum(sum(cm))
acc = (cm[0, 0] + cm[1, 1]) / total
sensitivity = cm[0, 0] / (cm[0, 0] + cm[0, 1])
specificity = cm[1, 1] / (cm[1, 0] + cm[1, 1])

# show the confusion matrix, accuracy, sensitivity, and specificity
print(cm)
print("acc: {:.4f}".format(acc))
print("sensitivity: {:.4f}".format(sensitivity))
print("specificity: {:.4f}".format(specificity))

# plot the training loss and accuracy
N = EPOCHS
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, N), H.history["accuracy"], label="train_acc")
plt.plot(np.arange(0, N), H.history["val_accuracy"], label="val_acc")
plt.title("Training Loss and Accuracy on COVID-19 Dataset")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="lower left")
plt.savefig(args["plot"])

# serialize the model to disk
print(f"[INFO] saving COVID-19 detector model on {model_name} data...")
model.save(model_name, save_format="h5")
