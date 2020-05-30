import argparse
import os
import warnings
warnings.filterwarnings("ignore")

import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.layers import (
    Activation, Conv3D, Dense, Dropout, Flatten, MaxPooling3D
)
from tensorflow.keras.callbacks import (
    EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
)
from tensorflow.keras.layers import LeakyReLU, BatchNormalization
from tensorflow.keras.losses import categorical_crossentropy
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
# from tensorflow.keras.utils.vis_utils import plot_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import classification_report, confusion_matrix

from videoto3d import Videoto3D
import pickle
import json


def main():
    parser = argparse.ArgumentParser(
        description='simple 3D convolution for action recognition'
    )
    parser.add_argument('--batch', type=int, default=8)
    parser.add_argument('--epoch', type=int, default=20)
    parser.add_argument(
        '--videos',
        type=str,
        default='../data/pocus_videos/convex',
        help='directory where videos are stored'
    )
    parser.add_argument(
        '--json', type=str, default="../data/video_input_data/cross_val.json"
    )
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--fold', type=int, default=0)
    parser.add_argument('--load', type=bool, default=False)
    parser.add_argument('--fr', type=int, default=5)
    parser.add_argument('--depth', type=int, default=5)
    args = parser.parse_args()

    # Out model directory
    MODEL_D = args.output
    if not os.path.isdir(args.output):
        os.makedirs(args.output)

    # Initialize video converter
    vid3d = Videoto3D(
        args.videos,
        width=100,
        height=100,
        depth=args.depth,
        framerate=args.fr
    )
    # Load saved data or read in videos
    if args.load:
        with open(
            "../data/video_input_data/vid_class_test100.dat", "rb"
        ) as infile:
            X_test, test_labels_text, test_files = pickle.load(infile)
        with open(
            "../data/video_input_data/vid_class_train100.dat", "rb"
        ) as infile:
            X_train, train_labels_text, train_files = pickle.load(infile)
    else:
        # Make split
        with open(args.json, "r") as infile:
            split_dict = json.load(infile)
        train_files, train_labels = split_dict[str(args.fold)]["train"]
        test_files, test_labels = split_dict[str(args.fold)]["test"]
        # # SPLIT NO CROSSVAL
        # class_short = ["cov", "pne", "reg"]
        # vid_files = [
        #     v for v in os.listdir(args.videos) if v[:3].lower() in class_short
        # ]
        # labels = [vid[:3].lower() for vid in vid_files]
        # train_files, test_files, train_labels, test_labels = train_test_split(
        #     vid_files, labels, stratify=labels, test_size=0.2
        # )
        # Read in videos and transform to 3D
        X_train, train_labels_text, train_files = vid3d.video3d(
            train_files,
            train_labels,
            save="../data/video_input_data/conv3d_train_fold_" +
            str(args.fold) + ".dat"
        )
        X_test, test_labels_text, test_files = vid3d.video3d(
            test_files,
            test_labels,
            save="../data/video_input_data/conv3d_test_fold_" +
            str(args.fold) + ".dat"
        )
    # One-hot encoding
    lb = LabelBinarizer()
    lb.fit(train_labels_text)
    Y_train = lb.transform(train_labels_text)
    Y_test = np.array(lb.transform(test_labels_text))
    # Verbose
    print("testing on split", args.fold)
    print(X_train.shape, Y_train.shape)
    print(X_test.shape, Y_test.shape)
    nb_classes = len(np.unique(train_labels_text))
    print(nb_classes, np.max(X_train))
    print("unique in train", np.unique(train_labels_text, return_counts=True))
    print("unique in test", np.unique(test_labels_text, return_counts=True))
    # Define callbacks
    earlyStopping = EarlyStopping(
        monitor='val_loss',
        patience=20,
        verbose=1,
        mode='min',
        restore_best_weights=True
    )

    mcp_save = ModelCheckpoint(
        os.path.join(MODEL_D, 'fold_' + str(args.fold) + '_epoch_{epoch:02d}'),
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

    # Define model
    model = Sequential()
    model.add(
        Conv3D(
            32,
            kernel_size=(3, 3, 3),
            input_shape=(X_train.shape[1:]),
            padding='same'
        )
    )
    model.add(Activation('relu'))
    model.add(Conv3D(32, kernel_size=(3, 3, 3), padding='same'))
    model.add(Activation('softmax'))
    model.add(MaxPooling3D(pool_size=(3, 3, 3), padding='same'))
    model.add(Dropout(0.5))

    model.add(Conv3D(32, kernel_size=(3, 3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv3D(32, kernel_size=(3, 3, 3), padding='same'))
    model.add(Activation('softmax'))
    model.add(MaxPooling3D(pool_size=(3, 3, 3), padding='same'))
    model.add(Dropout(0.5))

    model.add(Flatten())
    model.add(Dense(64, activation=None))
    model.add(BatchNormalization())
    model.add(Activation('sigmoid'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes, activation='softmax'))

    model.compile(
        loss=categorical_crossentropy, optimizer=Adam(), metrics=['accuracy']
    )
    model.summary()

    history = model.fit(
        X_train,
        Y_train,
        validation_data=(X_test, Y_test),
        batch_size=args.batch,
        epochs=args.epoch,
        verbose=1,
        shuffle=True,
        callbacks=[earlyStopping, mcp_save, reduce_lr_loss]
    )
    model.evaluate(X_test, Y_test, verbose=0)
    model_json = model.to_json()
    with open(
        os.path.join(args.output, '3dcnnmodel' + str(args.fold) + '.json'), 'w'
    ) as json_file:
        json_file.write(model_json)
    model.save_weights(
        os.path.join(args.output, '3dcnnmodel' + str(args.fold) + '.hd5')
    )

    loss, acc = model.evaluate(X_test, Y_test, verbose=0)
    print('Test loss:', loss)
    print('Test accuracy:', acc)

    print('Evaluating network...')
    predIdxs = model.predict(X_test, batch_size=args.batch)
    # for each image in the testing set we need to find the index of the
    # label with corresponding largest predicted probability
    predIdxs = np.argmax(predIdxs, axis=1)

    print('classification report sklearn:')
    print(
        classification_report(
            Y_test.argmax(axis=1), predIdxs, target_names=lb.classes_
        )
    )
    # compute the confusion matrix and and use it to derive the raw
    # accuracy, sensitivity, and specificity
    print('confusion matrix:')
    cm = confusion_matrix(Y_test.argmax(axis=1), predIdxs)
    print(cm)


if __name__ == '__main__':
    main()
