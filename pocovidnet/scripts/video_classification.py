import argparse
import json
import os
import pickle
import warnings

import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras.callbacks import (
    EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
)
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dense, GlobalAveragePooling3D
from tensorflow.keras.losses import categorical_crossentropy
from tensorflow.keras.models import Model
from pocovidnet.utils import fix_layers

from pocovidnet import VIDEO_MODEL_FACTORY
from pocovidnet.videoto3d import Videoto3D

warnings.filterwarnings("ignore")


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
        '--json', type=str, default="../data/cross_val.json"
    )
    parser.add_argument('--output', type=str, default="video_model_outputs")
    parser.add_argument('--fold', type=int, default=0)
    parser.add_argument('--load', type=bool, default=False)
    parser.add_argument('--fr', type=int, default=5)
    parser.add_argument('--depth', type=int, default=5)
    parser.add_argument('--model_id', type=str, default='genesis')
    parser.add_argument('--lr', type=float, default=1e-4)
    parser.add_argument('--trainable_base_layers', type=int, default=0)
    parser.add_argument(
        '--save', type=str, default='../data/video_input_data'
    )
    parser.add_argument(
        '--weight_path', type=str, default='../Genesis_Chest_CT.h5'
    )

    args = parser.parse_args()

    # Out model directory
    MODEL_D = args.output
    if not os.path.isdir(MODEL_D):
        if not os.path.exists(MODEL_D):
            os.makedirs(args.output)
    if not os.path.isdir(args.save):
        os.makedirs(args.save)

    # Initialize video converter
    vid3d = Videoto3D(
        args.videos, width=64, height=64, depth=args.depth, framerate=args.fr
    )
    # Load saved data or read in videos
    if args.load:
        with open(
            os.path.join(
                args.save, 'conv3d_test_fold_' + str(args.fold) + '.dat'
            ), 'rb'
        ) as infile:
            X_test, test_labels_text, test_files = pickle.load(infile)
        with open(
            os.path.join(
                args.save, 'conv3d_train_fold_' + str(args.fold) + '.dat'
            ), 'rb'
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
            save=os.path.join(
                args.save, "conv3d_train_fold_" + str(args.fold) + ".dat"
            )
        )
        X_test, test_labels_text, test_files = vid3d.video3d(
            test_files,
            test_labels,
            save=os.path.join(
                args.save, "conv3d_test_fold_" + str(args.fold) + ".dat"
            )
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
        os.path.join(MODEL_D, 'fold_' + str(args.fold), 'best_weights'),
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
    if args.model_id == 'base':
        input_shape = X_train.shape[1:]
        model = VIDEO_MODEL_FACTORY[args.model_id](input_shape, nb_classes)
    elif args.model_id == 'genesis':

        # For Genesis models inputs are shrinked to 64,64
        input_shape = 42
        input_shape = 1, 64, 64, 32

        X_train = np.transpose(X_train, [0, 4, 2, 3, 1])
        X_test = np.transpose(X_test, [0, 4, 2, 3, 1])
        # Frames are also repeated 6-7 times since depth of model is 32
        X_test = np.repeat(X_test, [6, 7, 7, 6, 6], axis=-1)
        X_train = np.repeat(X_train, [6, 7, 7, 6, 6], axis=-1)

        model = VIDEO_MODEL_FACTORY[args.model_id
                                    ](input_shape, batch_normalization=True)
        model.load_weights(args.weight_path)
        x = model.get_layer('depth_7_relu').output
        x = GlobalAveragePooling3D()(x)
        x = Dense(1024, activation='relu')(x)
        output = Dense(nb_classes, activation='softmax')(x)
        model = Model(inputs=model.input, outputs=output)
        model = fix_layers(
            model, num_flex_layers=args.trainable_base_layers + 4
        )

    print(model.summary())
    opt = Adam(lr=args.lr, decay=args.lr / args.epoch)
    model.compile(
        optimizer=opt, loss=categorical_crossentropy, metrics=['accuracy']
    )
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
        os.path.join(
            MODEL_D, 'fold_' + str(args.fold), '3dcnnmodel_final.json'
        ), 'w'
    ) as json_file:
        json_file.write(model_json)
    model.save_weights(
        os.path.join(
            MODEL_D, 'fold_' + str(args.fold), '3dcnnmodel_final.hd5'
        )
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
