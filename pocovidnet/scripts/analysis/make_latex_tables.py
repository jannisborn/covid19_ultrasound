import os
import pandas as pd

# Define paths to results files
base_dir = "../results_oct/"
models_to_evaluate = [
    "frame_based_3", "genesis_based_3"
    # "base_3", "cam_3", "nasnet_3", "encoding_3", "segmented_3"
]
vid_models_to_evaluate = ["frame_based_3", "genesis_based_3"]

print()
print("---------------------------------")
print("FRAME BASED EVALUATION")
print("---------------------------------")

class_map2 = {0: "COVID-19", 1: "Pneumonia", 2: "Healthy", 3: "Uninformative"}
for model in models_to_evaluate:
    mean_table = pd.read_csv(os.path.join(base_dir, model + "_mean.csv"))
    std_table = pd.read_csv(os.path.join(base_dir, model + "_std.csv"))
    print("----------", model, " ---------------")
    for i, row in mean_table.iterrows():
        std_row = std_table.loc[i]
        if i == 0:
            print(
                round(row["Accuracy"], 3), std_row["Accuracy"],
                row["Balanced"], round(std_row["Balanced"], 3)
            )
        print(
            "&",
            class_map2[i],
            "& $",
            round(row["Recall"], 2),
            "\\pm {\scriptstyle",
            std_row["Recall"],
            "}$ & $",
            round(row["Precision"], 2),
            "\\pm {\scriptstyle",
            std_row["Precision"],
            "}$ & $",
            round(row["F1-score"], 2),
            "\\pm {\scriptstyle",
            std_row["F1-score"],
            "}$ & $",
            round(row["Specificity"], 2),
            "\\pm {\scriptstyle",
            std_row["Specificity"],
            "}$",
        )
        # round(row["MCC"], 2),
        # "\\pm {\scriptstyle", std_row["MCC"], "} $ \\\\"
