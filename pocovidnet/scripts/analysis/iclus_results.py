import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
import seaborn as sn
from scipy.stats import pearsonr

severity_table = "../data/iclus_severity.csv"
take_dir = "best_of_both_crops"
res_dir = "results_oct/iclus/" + take_dir
res_dir_conf = "results_oct/iclus/iclus_results"
UNCERTAIN = 1
CUTOFF = 0.05
data_dir = "../data/ICLUS"

severity = pd.read_csv(severity_table, delimiter=";")
plot_boxplot = True
plot_cutoffs = False


def predict_label(logits, confidences, pred_conf, cutoff=0.6, per_model=False):
    # max_probs = np.max(logits, axis=1)
    if per_model:
        use_frames = np.zeros(confidences.shape).astype(bool)
        for i in range(5):
            quant = np.quantile(confidences[:, i], cutoff)
            use_frames[:, i] = confidences[:, i] > quant
        # eligible_frame_inds = np.mean(use_frames, axis=(0, 1)) > 0.5
        votes = pred_conf[use_frames]
        uni, count = np.unique(votes, return_counts=True)
        vid_lab = uni[np.argmax(count)]

    avg_conf = np.mean(confidences, axis=(0, 1))
    quantile_cutoff = np.quantile(avg_conf, cutoff)
    eligible_frame_inds = avg_conf > quantile_cutoff
    logits_restricted = logits[eligible_frame_inds]
    # frame prediction:
    argmax_probs = np.argmax(logits_restricted, axis=1)
    # vid prediction
    uni, count = np.unique(argmax_probs, return_counts=True)
    if not per_model:
        vid_lab = uni[np.argmax(count)]

    return vid_lab, argmax_probs

    # return np.argmax(np.mean(logits, axis=0))


# get convex
convex_table = severity[severity["filename"].str.contains("convex")]
convex_vids = convex_table["Video"]

# Make list of IDs that we analyze
process_vid_numbers = []
for subfolder in os.listdir(data_dir):
    if "linear" in subfolder.lower(
    ) or subfolder.startswith(".") or os.path.isfile(
        os.path.join(data_dir, subfolder)
    ):
        continue
    for vid in os.listdir(os.path.join(data_dir, subfolder)):
        vid_id = vid.split(".")[0]
        if vid.startswith("."):
            continue
        video_path = os.path.join(data_dir, subfolder, vid)

        # print(int(vid.split(".")[0]) in convex_vids)
        process_vid_numbers.append(int(vid.split(".")[0]))

# Check whether we cover all videos
for vid in convex_vids.values:
    if vid not in process_vid_numbers:
        print("In ICLUS tabelle but not in our folder:", vid)
for vid in process_vid_numbers:
    if vid not in convex_vids.values:
        print("In our folder but not in ICLUS:", vid)

# Make label dict:
iclus_labels = dict(zip(convex_table["Video"], convex_table["Score"]))

print("evaluating on ", len(iclus_labels.keys()), "files")

# EVALUATION
# # code to iterate over different confidence cutoffs:
# cutoffs = [0.05]  # np.arange(0.05, 0.1, 0.05)
# results = np.zeros((len(cutoffs), 4))
# for c, CUTOFF in enumerate(cutoffs):
print("------------------- cutoff", CUTOFF, "------------")
frame_gt, frame_preds = [], []
gt, preds, pred_probs = list(), list(), list()
for vid_id in iclus_labels.keys():
    in_path = os.path.join(res_dir, f"cam_{vid_id}.npy")  # changed
    if not os.path.exists(in_path):
        print("Warning: logits do not exist", in_path)
        continue
    confs = np.load(os.path.join(res_dir_conf, f"conf_{vid_id}.npy"))
    pred_conf = np.load(os.path.join(res_dir_conf, f"pred_{vid_id}.npy"))
    uni, counts = np.unique(pred_conf, return_counts=True)
    pred_conf_label = uni[np.argmax(counts)]

    logits = np.load(in_path)
    # prediction probability: avg logit prob for covid
    prob = np.mean(logits[:, 0])  # - np.mean(logits[:, 2])
    # other option: average confidences for covid
    # prob = np.mean(confs[pred_conf == 0])
    # if np.isnan(prob):
    #     prob = 0
    pred_label, pred_frame = predict_label(logits, confs, pred_conf, CUTOFF)
    # print(vid_id)
    # if pred_conf_label != pred_label:
    #     print("uncertainty label unqual!")
    #     print("conf: ", pred_conf_label, "normal", pred_label)
    #     print()
    # np.argmax(np.mean(logits, axis=0))  #
    # print(pred_label)
    gt.append(iclus_labels[vid_id])
    pred_probs.append(prob)
    preds.append(pred_label)
    if iclus_labels[vid_id] > 0:
        iclus_translated = 0
    else:
        iclus_translated = 2
    frame_gt.extend([iclus_translated for _ in range(len(pred_frame))])
    # [iclus_translated for _ in range(len(logits))])
    frame_preds.extend(pred_frame)
    # np.argmax(logits, axis=1).tolist())
    # logits[:, 0])
    # np.argmax(logits, axis=1).tolist())
    if (iclus_labels[vid_id] > 0 and pred_label
        == 2) or (iclus_labels[vid_id] == 0 and pred_label == 0):
        print(
            "wrong, severity is ", iclus_labels[vid_id], "but pred is",
            pred_label, "video:", vid_id
        )
    # print(gt[-1], preds[-1])

# correlation
print("Pearson correlation of scores:", pearsonr(gt, pred_probs))
frame_wise = accuracy_score(frame_gt, frame_preds)

# compute accuracy
correct = 0
all_covid = 0
tp = 0
prec = 0
# print(gt, preds)
for gt_lab, pred_lab in zip(gt, preds):
    if gt_lab > 0 and pred_lab == 0 or gt_lab == 0 and pred_lab == 2:
        correct += 1
    if pred_lab == 0:
        prec += 1
    if gt_lab > 0:
        all_covid += 1
        if pred_lab == 0:
            tp += 1
print("Accuracy: ", round(correct / len(preds), 3), correct, len(preds))
print("Sensitivity covid:", round(tp / float(all_covid), 3))
print("Precision covid", round(tp / float(prec), 3))
if plot_cutoffs:
    results[c, 0] = frame_wise
    print("Frame wise accuracy", frame_wise)
    results[c, 1] = round(correct / len(preds), 3)
    results[c, 2] = round(tp / float(all_covid), 3)
    results[c, 3] = round(tp / float(prec), 3)
# compute sensitivity

if plot_cutoffs:
    plt.figure(figsize=(10, 5))
    label = ["Frame wise acc", "Acc", "Sensitivity", "Precision"]
    for i in range(4):
        plt.plot(results[:, i], label=label[i])
    plt.xticks(np.arange(len(cutoffs)), [round(c, 2) for c in cutoffs])
    plt.legend()
    plt.savefig(f"results_oct/plots/dez_iclus_confidence_new.pdf")
    plt.show()

# Violin plot
if plot_boxplot:
    df = pd.DataFrame(
        np.swapaxes(np.array([gt, pred_probs]), 1, 0),
        columns=["Severity", "Predicted COVID probability"]
    )
    plt.figure(figsize=(10, 6))
    ax = sn.boxplot(x="Severity", y="Predicted COVID probability", data=df)
    colors = ['green', 'orange', 'orangered', 'firebrick']
    for box, col in zip(ax.artists, colors):
        # Change the appearance of that box
        box.set_facecolor(col)
        box.set_edgecolor('black')
        box.set_linewidth(2)
    plt.xlabel("Severity of abnormalities", fontsize=25)
    plt.ylabel("Predicted COVID-19 probability", fontsize=23)
    plt.ylim(0, 1)
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.yticks(fontsize=15)
    plt.xticks([0, 1, 2, 3], [0, 1, 2, 3], fontsize=20)
    plt.tight_layout()
    plt.savefig(f"results_oct/plots/dez_conf_{take_dir}.pdf")