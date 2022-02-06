from pocovidnet.evaluate_covid19 import Evaluator
import os
import numpy as np
import cv2
from imutils import paths
from sklearn.metrics import (
    classification_report, confusion_matrix, balanced_accuracy_score,
    accuracy_score, matthews_corrcoef
)
import pickle
import pandas as pd
import argparse

CLASS_MAPPING = {
    3: ['covid', 'pneumonia', 'regular'],
    4: ['covid', 'pneumonia', 'regular', 'uninformative']
}


def mcc_multiclass(y_true, y_pred):
    """
    MCC score for multiclass problem
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    mcc_out = []
    for classe in np.unique(y_true):
        y_true_binary = (y_true == classe).astype(int)
        y_pred_binary = (y_pred == classe).astype(int)
        mcc_out.append(matthews_corrcoef(y_true_binary, y_pred_binary))
    return mcc_out


def specificity(y_true, y_pred):
    """
    Compute specificity for multiclass predictions
    """
    # true negatives / negatives
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    spec_out = []
    for classe in np.unique(y_true):
        negatives = np.sum((y_true != classe).astype(int))
        tn = np.sum((y_pred[y_true != classe] != classe).astype(int))
        spec_out.append(tn / negatives)
    return spec_out


def load_encoding(imagePath, FEAT_ID=0, w=7, h=9, pool=True):
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
        image = cv2.resize(data['f' + str(feat)][0, :, :, :], (w, h))
        sp = np.mean(image, axis=(0, 1)) if pool else image.flatten()
        sample.append(sp)
    sample = np.concatenate(sample).flatten()
    return sample


def evaluate_logits(saved_logits, saved_gt, saved_files, CLASSES, save_path):
    all_reports, accs, bal_accs = [], [], []
    for s in range(len(saved_logits)):
        gt_s = saved_gt[s]
        pred_idx_s = np.argmax(np.array(saved_logits[s]), axis=1)
        report = classification_report(
            gt_s, pred_idx_s, target_names=CLASSES, output_dict=True
        )
        mcc_scores = mcc_multiclass(gt_s, pred_idx_s)
        spec_scores = specificity(gt_s, pred_idx_s)
        for i, cl in enumerate(CLASSES):
            report[cl]["mcc"] = mcc_scores[i]
            report[cl]["specificity"] = spec_scores[i]
        df = pd.DataFrame(report).transpose()
        df = df.drop(columns="support")
        df["accuracy"] = [report["accuracy"] for _ in range(len(df))]
        bal = balanced_accuracy_score(gt_s, pred_idx_s)
        df["balanced"] = [bal for _ in range(len(df))]
        accs.append(report["accuracy"])
        bal_accs.append(balanced_accuracy_score(gt_s, pred_idx_s))
        all_reports.append(np.array(df)[:len(CLASSES)])

    print("Average scores in cross validation:")
    df_arr = np.around(np.mean(all_reports, axis=0), 3)
    df_classes = pd.DataFrame(
        df_arr,
        columns=[
            "Precision", "Recall", "F1-score", "MCC", "Specificity",
            "Accuracy", "Balanced"
        ],
        index=CLASSES
    )
    print(df_classes)
    df_classes.to_csv(save_path + "_mean.csv")

    print("Standard deviations:")
    df_std = np.around(np.std(all_reports, axis=0), 2)
    df_std = pd.DataFrame(
        df_std,
        columns=[
            "Precision", "Recall", "F1-score", "MCC", "Specificity",
            "Accuracy", "Balanced"
        ],
        index=CLASSES
    )
    df_std.to_csv(save_path + "_std.csv")
    print(df_std)


def evaluate_3(saved_logits, saved_gt, saved_files, CLASSES, save_path):
    new_logits, new_gt, new_files = [], [], []
    counter = 0
    for i in range(5):
        gt_inds = np.where(np.array(saved_gt[i]) < 3)[0]
        counter += len(gt_inds)
        new_logits.append(np.array(saved_logits[i])[gt_inds, :3])
        new_gt.append(np.array(saved_gt[i])[gt_inds])
        new_files.append(np.array(saved_files[i])[gt_inds])

    with open(save_path + "_3.dat", "wb") as outfile:
        pickle.dump((new_logits, new_gt, new_files), outfile)
    evaluate_logits(new_logits, new_gt, new_files, CLASSES, save_path + "_3")


def main():
    parser = argparse.ArgumentParser(description='Evaluate cross validation')
    parser.add_argument('--data', type=str, default="../data/cross_validation")
    parser.add_argument('--weights', type=str, default='trained_models')
    parser.add_argument('--m_id', type=str, default='vgg_base')
    parser.add_argument('--classes', type=int, default=4)
    parser.add_argument('--folds', type=int, default=5)
    parser.add_argument('--save_path', type=str, default="results_vgg")
    args = parser.parse_args()

    saved_logits, saved_gt, saved_files = [], [], []

    CLASSES = CLASS_MAPPING[args.classes]
    MOD_FILE_MAP = {
        'dense': ['npz'],
        'vgg_base': ['gif', 'jpg', 'png', 'peg'],
        'vgg_cam': ['jpg', 'png', 'peg'],
        'nasnet': ['jpg', 'png', 'peg'],
        'mobilenet_v2': ['jpg', 'png', 'peg']
    }

    for i in range(args.folds):
        print("------------- SPLIT ", i, "-------------------")
        # define data input path
        path = os.path.join(args.data, "split" + str(i))

        test_labels, test_files = [], []
        test_data = []

        # loop over the image paths (train and test)
        for imagePath in paths.list_files(path):
            # select the correct files
            if imagePath[-3:] not in MOD_FILE_MAP[args.m_id]:
                continue

            # extract the class label from the filename
            label = imagePath.split(os.path.sep)[-2]

            # load the image
            if args.m_id == 'dense':
                image = load_encoding(imagePath)
            elif imagePath[-3:] == 'gif':
                cap = cv2.VideoCapture(imagePath)
                ret, image = cap.read()
            else:
                image = cv2.imread(imagePath)

            # update the data and labels lists, respectively
            test_labels.append(label)
            test_data.append(image)
            test_files.append(imagePath.split(os.path.sep)[-1])

        if args.m_id == 'dense':
            test_data = np.expand_dims(np.stack(test_data), 1)
            preprocess = False
        else:
            preprocess = True

        # build ground truth data
        gt_class_idx = np.array([CLASSES.index(lab) for lab in test_labels])
        model = None
        # load model
        model = Evaluator(
            weights_dir=args.weights,
            ensemble=False,
            split=i,
            num_classes=len(CLASSES),
            model_id=args.m_id
        )
        print("testing on n_files:", len(test_data))

        # MAIN STEP: feed through model and compute logits
        logits = np.array(
            [model(img, preprocess=preprocess) for img in test_data]
        )

        # remember for evaluation:
        saved_logits.append(logits)
        saved_gt.append(gt_class_idx)
        saved_files.append(test_files)

        # output the information
        predIdxs = np.argmax(logits, axis=1)

        print(
            classification_report(
                gt_class_idx, predIdxs, target_names=CLASSES
            )
        )

    with open(args.save_path + ".dat", "wb") as outfile:
        pickle.dump((saved_logits, saved_gt, saved_files), outfile)

    # EVALUATE
    evaluate_logits(
        saved_logits, saved_gt, saved_files, CLASSES, args.save_path
    )

    # EVALUATE ONLY 3 CLASSES
    if len(CLASSES) == 4:
        evaluate_3(
            saved_logits, saved_gt, saved_files, CLASS_MAPPING[3],
            args.save_path
        )


if __name__ == "__main__":
    main()
