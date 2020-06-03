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


def main():
    parser = argparse.ArgumentParser(description='Evaluate cross validation')
    parser.add_argument('--data', type=str, default="../data/cross_validation")
    parser.add_argument('--weights', type=str, default='trained_models')
    parser.add_argument('--m_id', type=str, default='vgg_base')
    parser.add_argument('--classes', type=int, default=4)
    parser.add_argument('--folds', type=int, default=5)
    parser.add_argument('--save_path', type=str, default="logits.dat")
    args = parser.parse_args()

    saved_logits, saved_gt, saved_files = [], [], []

    CLASSES = CLASS_MAPPING[args.classes]

    for i in range(args.folds):
        print("------------- SPLIT ", i, "-------------------")
        # define data input path
        path = os.path.join(args.data, "split" + str(i))

        test_labels, test_files = [], []
        test_data = []

        # loop over the image paths (train and test)
        for imagePath in paths.list_images(path):

            # extract the class label from the filename
            label = imagePath.split(os.path.sep)[-2]

            # load the image
            image = cv2.imread(imagePath)

            # update the data and labels lists, respectively
            test_labels.append(label)
            test_data.append(image)
            test_files.append(imagePath.split(os.path.sep)[-1])

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
        logits = np.array([model(img) for img in test_data])

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

    with open(args.save_path, "wb") as outfile:
        pickle.dump((logits, gt_class_idx, test_files), outfile)

    # EVALUATE
    all_reports, accs, bal_accs = [], [], []
    for s in range(5):
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
    print(df_std)


if __name__ == "__main__":
    main()
