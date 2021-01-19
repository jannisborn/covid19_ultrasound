from sklearn.metrics import roc_auc_score, precision_score, recall_score, auc
from sklearn.metrics import confusion_matrix
import os
import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import pickle

OUT_DIR = "../results_oct/plots/new"
IN_DIR = "../results_oct/"
BEST_MODEL = "base_3.dat"

compare_model_list = [
    "base_3.dat", "cam_3.dat", "nasnet_3.dat", "encoding_3.dat",
    "segmented_3.dat"
]
name_dict = {
    "base_3": "VGG",
    "cam_3": "VGG-CAM",
    "nasnet_3": "NASNetMobile",
    "encoding_3": "Segment-Enc",
    "segmented_3": "VGG-Segment"
}

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

from matplotlib import rc
plt.rcParams['legend.title_fontsize'] = 20
plt.rcParams['axes.facecolor'] = 'white'
# activate latex text rendering
rc('text', usetex=False)


def data_to_label(data, text):
    return (
        np.asarray(
            [
                "{0:.2f}\n".format(data) + u"\u00B1" + "{0:.2f}".format(text)
                for data, text in zip(data.flatten(), text.flatten())
            ]
        )
    ).reshape(3, 3)


def plot_confusion_matrix(data_confusion, labels, save_path):
    fig = plt.figure(figsize=(6, 5))
    ax = fig.axes
    df_cm = pd.DataFrame(
        data_confusion,
        index=[i for i in ["COVID-19", "Bact. Pneu.", "Healthy"]],
        columns=[i for i in ["COVID-19", "Bact. Pneu.", "Healthy"]]
    )

    sn.set(font_scale=1.8)

    plt.xticks(
        np.arange(3) + 0.5, ("COVID-19", "Bact. Pneu.", "Normal"),
        fontsize="17",
        va="center"
    )
    plt.yticks(
        np.arange(3) + 0.5, ("C", "P", "H"),
        rotation=0,
        fontsize="17",
        va="center"
    )
    # sn.heatmap(df_cm, annot=True, fmt="g", cmap="YlGnBu")
    sn.heatmap(df_cm, annot=labels, fmt='', cmap="YlGnBu")
    # ax.xaxis.tick_bottom()
    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        top=False,  # ticks along the top edge are off
        labelbottom=True
    )
    plt.xlabel("$\\bf{Predictions}$", fontsize=23)
    plt.ylabel("$\\bf{Ground\ truth}$", fontsize=23)
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0, transparent=True)


base_eval_points = np.linspace(0, 1, 200, endpoint=True)


def roc_auc(saved_logits, saved_gt):
    data, scores, roc_auc_std = [], [], []
    max_points = []
    for i in range(3):
        out_roc = np.zeros((5, len(base_eval_points)))
        out_prec = np.zeros((5, len(base_eval_points)))

        roc_auc = []
        max_acc = []

        # Iterate over folds
        for k in range(5):
            # get binary predictions for this class
            gt = (saved_gt[k] == i).astype(int)
            # pred = saved_logits[k][:, i]
            if np.any(saved_logits[k] < 0):
                pred = np.exp(np.array(saved_logits[k]))[:, i]
            else:
                pred = np.array(saved_logits[k])[:, i]

            roc_auc.append(roc_auc_score(gt, pred))

            precs, recs, fprs, julie_points = [], [], [], []
            for j, thresh in enumerate(
                np.linspace(0, 1.1, 100, endpoint=True)
            ):
                preds_thresholded = (pred > thresh).astype(int)
                tp = np.sum(preds_thresholded[gt == 1])
                p = np.sum(gt)
                n = len(gt) - p
                fp = np.sum(preds_thresholded[gt == 0])
                inverted = np.absolute(preds_thresholded - 1)
                tn = np.sum(inverted[gt == 0])
                fn = np.sum(inverted[gt == 1])
                fpr = fp / float(n)
                tpr = tp / float(p)

                if tp + fp == 0:
                    precs.append(1)
                else:
                    precs.append(tp / (tp + fp))
                recs.append(tpr)
                fprs.append(fpr)
                julie_points.append((tp + tn) / (tp + tn + fp + fn))

            # clean
            recs = np.asarray(recs)
            precs = np.asarray(precs)
            fprs = np.asarray(fprs)
            sorted_inds = np.argsort(recs)
            # prepare for precision-recall curve
            precs_sorted = precs[sorted_inds]
            recs_sorted = recs[sorted_inds]
            precs_cleaned = precs_sorted[recs_sorted > 0]
            recs_cleaned = recs_sorted[recs_sorted > 0]
            precs_inter = np.interp(
                base_eval_points, recs_cleaned, precs_cleaned
            )
            # prepare for roc-auc curve
            sorted_inds = np.argsort(fprs)
            recs_fpr_sorted = recs[sorted_inds]
            fprs_sorted = fprs[sorted_inds]
            roc_inter = np.interp(
                base_eval_points, fprs_sorted, recs_fpr_sorted
            )
            # append current fold
            out_prec[k] = precs_inter
            out_roc[k] = roc_inter

            # compute recall of max acc:
            max_acc.append(recs[np.argmax(julie_points)])

        # out_curve = np.mean(np.asarray(out_curve), axis=0)

        prec_mean = np.mean(out_prec, axis=0)
        prec_std = np.std(out_prec, axis=0)
        roc_mean = np.mean(out_roc, axis=0)
        roc_std = np.std(out_roc, axis=0)

        # append scores
        scores.append(round(np.mean(roc_auc), 2))
        roc_auc_std.append(round(np.std(roc_auc), 2))

        # point of maximum accuracy
        max_points.append(np.mean(max_acc))

        data.append((roc_mean, roc_std, prec_mean, prec_std))
    return data, max_points, scores, roc_auc_std


def closest(in_list, point):
    return np.argmin(np.absolute(np.asarray(in_list) - point))


# ------------------- ROC AUC BEST MODEL ------------------------------

with open(os.path.join(IN_DIR, BEST_MODEL), "rb") as outfile:
    (saved_logits, saved_gt, saved_files) = pickle.load(outfile)

data, max_points, scores, roc_auc_std = roc_auc(saved_logits, saved_gt)

cols = ["red", "orange", "green"]
classes = ["COVID-19", "Bacterial Pneu.", "Healthy"]

# ROC curve of best model
plt.figure(figsize=(6, 5))
plt.plot([0, 1], [0, 1], color='grey', lw=1.5, linestyle='--')
for i in range(3):
    roc_mean, roc_std, _, _ = data[i]
    lab = classes[i] + " (%.2f" % scores[i] + "$\pm$" + str(
        roc_auc_std[i]
    ) + ")"
    plt.plot(base_eval_points, roc_mean, 'k-', c=cols[i], label=lab, lw=3)
    # print(len(r), max_points[i])
    # print(base_eval_points[closest(roc_mean, max_points[i])], max_points[i])
    plt.scatter(
        base_eval_points[closest(roc_mean, max_points[i])],
        max_points[i],
        s=150,
        marker="o",
        c=cols[i]
    )
    plt.fill_between(
        base_eval_points,
        roc_mean - roc_std,
        roc_mean + roc_std,
        alpha=0.1,
        facecolor=cols[i]
    )
    plt.ylim(0, 1.03)
plt.xlim(-0.02, 1)
plt.ylabel("$\\bf{Sensitivity}$", fontsize=25)
plt.xlabel("$\\bf{False\ positive\ rate}$", fontsize=25)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.legend(
    fontsize=16, title="    $\\bf{Class}\ \\bf(AUC)}$"
)  # "\n  $\\bf{(o:\ maximal\ accuracy)}$")
plt.savefig(
    os.path.join(OUT_DIR, "roc_curve.pdf"),
    bbox_inches='tight',
    pad_inches=0,
    transparent=True
)

# ------------------- PREC REC BEST MODEL ------------------------------

# PREC REC curve of best model
plt.figure(figsize=(6, 5))
plt.plot([1, 0], [0, 1], color='grey', lw=1.5, linestyle='--')
for i in range(3):
    _, _, prec_mean, prec_std = data[i]
    prec_rec_auc = auc(base_eval_points, prec_mean)
    auc_stdup = abs(auc(base_eval_points, prec_mean + prec_std) - prec_rec_auc)
    auc_stddown = abs(
        auc(base_eval_points, prec_mean + prec_std) - prec_rec_auc
    )
    # lab = classes[i]
    lab = classes[i] + " (%.2f" % prec_rec_auc + "$\pm$" + str(
        round(np.mean([auc_stdup, auc_stddown]), 2)
    ) + ")"
    plt.plot(base_eval_points, prec_mean, 'k-', c=cols[i], label=lab, lw=3)
    plt.fill_between(
        base_eval_points,
        prec_mean - prec_std,
        prec_mean + prec_std,
        alpha=0.1,
        facecolor=cols[i]
    )
plt.ylim(0, 1.03)
plt.xlim(-0.02, 1)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.ylabel("$\\bf{Precision}$", fontsize=25)
plt.xlabel("$\\bf{Recall}$", fontsize=25)
plt.legend(
    fontsize=18,
    title="    $\\bf{Class}\ \\bf(AUC)}$"  # "    $\\bf{Class}$"
)  # "\n  $\\bf{(o:\ maximal\ accuracy)}$")
# plt.title("$\\bf{ROC\ curves}$", fontsize=15)
plt.savefig(
    os.path.join(OUT_DIR, "prec_rec_curves.pdf"),
    bbox_inches='tight',
    pad_inches=0,
    transparent=True
)

# ------------------- ROC AUC ALL MODELS ------------------------------
for CLASS in range(3):
    cols = ["red", "orange", "green", "blue", "purple"]
    classes = ["COVID-19", "Bacterial Pneu.", "Healthy"]
    # roc_auc_scores = np.mean(np.asarray(scores), axis=0)
    fig = plt.figure(figsize=(6, 5))
    # plt.subplot(1,3,1)
    plt.plot([0, 1], [0, 1], color='grey', lw=1.5, linestyle='--')
    for i, model_data in enumerate(compare_model_list):
        with open(os.path.join(IN_DIR, model_data), "rb") as outfile:
            (saved_logits, saved_gt, saved_files) = pickle.load(outfile)
        data, max_points, scores, roc_auc_std = roc_auc(saved_logits, saved_gt)
        roc_mean, roc_std, _, _ = data[CLASS]
        lab = name_dict[model_data.split(".")[0]
                        ] + " (%.2f" % scores[CLASS] + "$\pm$" + str(
                            roc_auc_std[CLASS]
                        ) + ")"

        plt.plot(base_eval_points, roc_mean, 'k-', c=cols[i], label=lab, lw=3)
        plt.scatter(
            base_eval_points[closest(roc_mean, max_points[CLASS])],
            max_points[CLASS],
            s=150,
            marker="o",
            c=cols[i]
        )
        plt.fill_between(
            base_eval_points,
            roc_mean - roc_std,
            roc_mean + roc_std,
            alpha=0.1,
            facecolor=cols[i]
        )
    plt.ylim(0, 1.01)
    plt.xlim(-0.02, 1)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.ylabel("$\\bf{Sensitivity}$", fontsize=25)
    plt.xlabel("$\\bf{False\ positive\ rate}$", fontsize=25)
    plt.legend(
        fontsize=14, title="    $\\bf{Model}\ \\bf(ROC-AUC)}$"
    )  # "\n  $\\bf{(o:\ maximal\ accuracy)}$")
    # plt.title("ROC-curve (COVID-19)", fontsize=20)
    plt.savefig(
        os.path.join(OUT_DIR, "roc_curve" + str(CLASS) + ".pdf"),
        bbox_inches='tight',
        pad_inches=0,
        transparent=True
    )

    # ------------------- PREC REC ALL MODELS ------------------------------

    fig = plt.figure(figsize=(6, 5))

    for i, model_data in enumerate(compare_model_list):
        with open(os.path.join(IN_DIR, model_data), "rb") as outfile:
            (saved_logits, saved_gt, saved_files) = pickle.load(outfile)
        data, max_points, scores, roc_auc_std = roc_auc(saved_logits, saved_gt)
        _, _, prec_mean, prec_std = data[CLASS]
        # lab = name_dict[model_data.split(".")[0]]
        # compute auc
        prec_rec_auc = auc(base_eval_points, prec_mean)
        auc_stdup = abs(
            auc(base_eval_points, prec_mean + prec_std) - prec_rec_auc
        )
        auc_stddown = abs(
            auc(base_eval_points, prec_mean + prec_std) - prec_rec_auc
        )
        # define label
        lab = name_dict[model_data.split(".")[0]
                        ] + " (%.2f" % prec_rec_auc + "$\pm$" + str(
                            round(np.mean([auc_stdup, auc_stddown]), 2)
                        ) + ")"
        plt.plot(base_eval_points, prec_mean, 'k-', c=cols[i], label=lab, lw=3)
        plt.fill_between(
            base_eval_points,
            prec_mean - prec_std,
            prec_mean + prec_std,
            alpha=0.1,
            facecolor=cols[i]
        )
    plt.ylim(0, 1.01)
    plt.xlim(-0.02, 1.02)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.ylabel("$\\bf{Precision}$", fontsize=25)
    plt.xlabel("$\\bf{Recall}$", fontsize=25)
    plt.legend(fontsize=14, title="    $\\bf{Model}\ \\bf(AUC)}$")

    plt.savefig(
        os.path.join(OUT_DIR, "prec_rec_" + str(CLASS) + ".pdf"),
        bbox_inches='tight',
        pad_inches=0,
        transparent=True
    )

# ------------------- CONFUSION MATRICES ------------------------------

with open(os.path.join(IN_DIR, BEST_MODEL), "rb") as outfile:
    (saved_logits, saved_gt, saved_files) = pickle.load(outfile)

all_cms = np.zeros((5, 3, 3))
for s in range(5):
    # print(saved_files[s])
    gt_s = saved_gt[s]
    pred_idx_s = np.argmax(np.array(saved_logits[s]), axis=1)
    assert len(gt_s) == len(pred_idx_s)
    cm = np.array(confusion_matrix(gt_s, pred_idx_s))
    all_cms[s] = cm

# ABSOLUTE
data_confusion = np.sum(all_cms, axis=0).astype(int)
plot_confusion_matrix(
    data_confusion, True, os.path.join(OUT_DIR, "conf_matrix_abs.pdf")
)

# PRECISION
data_confusion = all_cms.copy()
for i in range(5):
    data_confusion[i] = data_confusion[i] / np.sum(data_confusion[i], axis=0)
prec_stds = np.std(data_confusion, axis=0)
data_confusion = np.mean(data_confusion, axis=0)
labels = data_to_label(data_confusion, prec_stds)
plot_confusion_matrix(
    data_confusion, labels, os.path.join(OUT_DIR, "conf_matrix_prec.pdf")
)

# SENSITIVITY
data_confusion = all_cms.copy()
for i in range(5):
    sums_axis = np.sum(data_confusion[i], axis=1)
    data_confusion[i] = np.array(
        [data_confusion[i, j, :] / sums_axis[j] for j in range(3)]
    )
sens_stds = np.std(data_confusion, axis=0)
data_confusion = np.mean(data_confusion, axis=0)
labels = data_to_label(data_confusion, sens_stds)
plot_confusion_matrix(
    data_confusion, labels, os.path.join(OUT_DIR, "conf_matrix_sens.pdf")
)
