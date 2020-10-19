import pickle
from sklearn.metrics import (
    classification_report, matthews_corrcoef, balanced_accuracy_score
)
import os
import pandas as pd
import numpy as np
import json
IN_DIR = "evaluation_outputs.dat"
OUT_DIR = "results_oct"
CROSS_VAL = "../data/cross_val.json'"

with open(IN_DIR, "rb") as infile:
    vidbased, frame_based = pickle.load(infile)

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


# define GT
lab_dict = {"cov": 0, "pne": 1, "reg": 2}
this_class = {"cov": "covid", "pne": "pneumonia", "reg": "regular"}
saved_gt = []

for i in range(5):
    all_labels = []
    files, labs = cross_val_split[str(i)]["test"]
    for j in range(len(files)):
        if "Butterfly" not in files[j]:
            assert os.path.exists(
                os.path.join(
                    "../data/cross_validation/split" + str(i),
                    this_class[labs[j]], files[j] + "_frame0.jpg"
                )
            ), files[j] + "_" + str(i)
        all_labels.append(lab_dict[labs[j]])
    saved_gt.append(all_labels)

# Evaluate
for classifier, name in zip(
    [frame_based, vidbased], ["frame_based", "genesis_based"]
):

    saved_logits = [[] for _ in range(5)]
    split_counter = 0
    frame_counter = len(saved_gt[0])
    for vid_ind in range(len(vidbased)):
        # print(frame_based[vid_ind].shape)
        # print(vid_ind, split_counter)
        saved_logits[split_counter].append(
            np.argmax(np.mean(classifier[vid_ind], axis=0))
        )
        if len(saved_logits[split_counter]) == len(saved_gt[split_counter]):
            # next cross val split
            # print(vid_ind, len(saved_gt[split_counter]), split_counter)
            frame_counter += len(saved_gt[split_counter])
            split_counter += 1
    assert len(saved_logits[2]) == len(saved_gt[2])

    all_reports = []
    accs = []
    bal_accs = []
    for s in range(5):
        gt_s = saved_gt[s]
        print(len(gt_s), saved_logits[s])
        pred_idx_s = saved_logits[
            s]  # np.argmax(np.array(saved_logits[s]), axis=1)
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
        # df["video"] = vid_accs[s]
        # df["video_balanced"] = vid_accs_bal[s]
        # print(df[:len(CLASSES)])
        #print(report["accuracy"])
        # print(np.array(df)[:3,:])
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
