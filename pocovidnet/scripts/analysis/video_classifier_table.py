import pickle
from sklearn.metrics import (
    classification_report, matthews_corrcoef, balanced_accuracy_score
)
import os
import pandas as pd
import numpy as np
import json
IN_DIR = "../models/evaluation_outputs_base.dat"
OUT_DIR = "../results_oct"
CROSS_VAL = "../../data/cross_val.json"

with open(IN_DIR, "rb") as infile:
    vidbased, frame_based = pickle.load(infile)
print(len(frame_based), frame_based[0].shape)
with open(CROSS_VAL, "r") as infile:
    cross_val_split = json.load(infile)

CLASSES = ['covid', 'pneumonia', 'regular']


def mcc_multiclass(y_true, y_pred):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    mcc_out = []
    for classe in np.unique(y_true):
        y_true_binary = (y_true == classe).astype(int)
        y_pred_binary = (y_pred == classe).astype(int)
        mcc_out.append(matthews_corrcoef(y_true_binary, y_pred_binary))
    return mcc_out


def specificity(y_true, y_pred):
    # true negatives / negatives
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    spec_out = []
    for classe in np.unique(y_true):
        negatives = np.sum((y_true != classe).astype(int))
        tn = np.sum((y_pred[y_true != classe] != classe).astype(int))
        spec_out.append(tn / negatives)
    return spec_out


def summarize_votes(logits):
    # option 1: mean
    # return np.argmax(np.mean(logits_current, axis=0))
    # option 2: majority vote
    votes = np.argmax(logits_current, axis=1)
    uni, counts = np.unique(votes, return_counts=True)
    return uni[np.argmax(counts)]


# define GT
lab_dict = {"cov": 0, "pne": 1, "reg": 2}
this_class = {"cov": "covid", "pne": "pneumonia", "reg": "regular"}
saved_gt = []
saved_files = []
for i in range(5):
    all_labels, all_files = [], []
    files, labs = cross_val_split[str(i)]["test"]
    for j in range(len(files)):
        assert os.path.exists(
            os.path.join(
                "../../data/cross_validation/split" + str(i),
                this_class[labs[j]], files[j] + "_frame0.jpg"
            )
        ), files[j] + " split: " + str(i)
        all_labels.append(lab_dict[labs[j]])
        all_files.append(files[j])
    saved_gt.append(all_labels)
    saved_files.append(all_files)

# Evaluate
for classifier, name in zip(
    [frame_based, vidbased], ["frame_based", "genesis_based"]
):
    saved_logits = [[] for _ in range(5)]
    split_counter = 0
    for vid_ind in range(len(vidbased)):
        if name == "genesis_based":
            logits_current = classifier[vid_ind][0]
        else:
            logits_current = classifier[vid_ind]
        saved_logits[split_counter].append(summarize_votes(logits_current))

        if len(saved_logits[split_counter]) == len(saved_gt[split_counter]):
            split_counter += 1
    assert len(saved_logits[4]) == len(
        saved_gt[4]
    ), "more files in json than in logits - check for errornous files in eval"

    all_reports = []
    accs = []
    bal_accs = []
    for s in range(5):
        gt_s = saved_gt[s]
        pred_idx_s = np.array(saved_logits[s])
        # get rid of uninformatives in video classification
        pred_idx_s[pred_idx_s == 3] = 2
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
        # df = np.array(report)
        all_reports.append(np.array(df)[:len(CLASSES)])
    df_arr = np.around(np.mean(all_reports, axis=0), 2)
    df_classes = pd.DataFrame(
        df_arr,
        columns=[
            "Precision", "Recall", "F1-score", "MCC", "Specificity",
            "Accuracy", "Balanced"
        ],
        index=CLASSES
    )
    print(df_classes)
    df_std = np.around(np.std(all_reports, axis=0), 2)
    df_std = pd.DataFrame(
        df_std,
        columns=[
            "Precision", "Recall", "F1-score", "MCC", "Specificity",
            "Accuracy", "Balanced"
        ],
        index=CLASSES
    )

    df_classes = df_classes[[
        "Accuracy", "Balanced", "Precision", "Recall", "Specificity",
        "F1-score", "MCC"
    ]]
    df_std = df_std[[
        "Accuracy", "Balanced", "Precision", "Recall", "Specificity",
        "F1-score", "MCC"
    ]]

    df_classes.to_csv(os.path.join(OUT_DIR, f"{name}_3_mean.csv"))
    df_std.to_csv(os.path.join(OUT_DIR, f"{name}_3_std.csv"))
