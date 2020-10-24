import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
import seaborn as sn
from scipy.stats import pearsonr

severity_table = "../data/iclus_severity.csv"
take_dir = "base"
res_dir = "results_oct/iclus/" + take_dir

data_dir = "../data/ICLUS"

severity = pd.read_csv(severity_table, delimiter=";")


def predict_label(logits, cutoff=0.6):
    # max_probs = np.max(logits, axis=1)
    # argmax_probs = np.argmax(logits, axis=1)
    # uni, count = np.unique(
    #     argmax_probs[max_probs > cutoff], return_counts=True
    # )
    # return uni[np.argmax(count)]
    return np.argmax(np.mean(logits, axis=0))


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
frame_gt, frame_preds = [], []
gt, preds, pred_probs = list(), list(), list()
print("gt   pred")
for vid_id in iclus_labels.keys():
    in_path = os.path.join(res_dir, f"cam_{vid_id}.npy")  # changed
    if not os.path.exists(in_path):
        print("Warning: logits do not exist", in_path)
        continue
    logits = np.load(in_path)
    prob = np.mean(logits[:, 0])  # - np.mean(logits[:, 2])
    pred_label = predict_label(logits)
    # np.argmax(np.mean(logits, axis=0))  #
    # print(pred_label)
    gt.append(iclus_labels[vid_id])
    pred_probs.append(prob)
    preds.append(pred_label)
    if iclus_labels[vid_id] > 0:
        iclus_translated = 0
    else:
        iclus_translated = 2
    frame_gt.extend([iclus_labels[vid_id] for _ in range(len(logits))])
    # [iclus_translated for _ in range(len(logits))])
    frame_preds.extend(np.argmax(logits, axis=1).tolist())
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

# Violin plot
df = pd.DataFrame(
    np.swapaxes(np.array([gt, pred_probs]), 1, 0),
    columns=["Severity", "Predicted COVID probability"]
)

ax = sn.boxplot(x="Severity", y="Predicted COVID probability", data=df)
colors = ['green', 'orange', 'orangered', 'firebrick']
for box, col in zip(ax.artists, colors):
    # Change the appearance of that box
    box.set_facecolor(col)
    box.set_edgecolor('black')
    box.set_linewidth(2)
plt.xlabel("Severity of abnormalities", fontsize=15)
plt.ylabel("Predicted COVID-19 probability", fontsize=15)
plt.ylim(0, 1)
plt.xticks([0, 1, 2, 3], [0, 1, 2, 3], fontsize=15)
plt.savefig(f"results_oct/plots/violin_iclus_{take_dir}.pdf")
plt.show()

print("Frame wise accuracy", accuracy_score(frame_gt, frame_preds))

# compute accuracy
correct = 0
all_covid = 0
tp = 0
prec = 0
print(gt, preds)
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
# compute sensitivity
