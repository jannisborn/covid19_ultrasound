import shutil
import numpy as np
import pandas as pd
import os
import json

base = "../../data/"
metadata = base + "dataset_metadata.csv"
out = "missing_MD_comments_jan"
if out is not None:
    os.makedirs(out)

# Analyze numbers in dataset
base_dir = "../../data/"
out_table = pd.DataFrame(index=['cov', 'pne', 'reg', 'vir'])
for modality in ["convex", "linear"]:
    for datatype in ["videos", "images"]:
        path = os.path.join(base_dir, "pocus_" + datatype, modality)
        file_list = filter(
            lambda x: (
                x[0] != "." and os.path.isfile(os.path.join(path, x)) and
                not "_Butterfly" in x
            ), os.listdir(path)
        )
        label_list = [f[:3].lower() for f in file_list]
        counts = [
            label_list.count(lab) for lab in ['cov', 'pne', 'reg', 'vir']
        ]
        out_table[modality + "_" + datatype] = counts
print("Data without Butterfly:")
print(out_table)

# add butterfly data
with open("../../data/data_from_butterfly.json", "r") as infile:
    butterfly = json.load(infile)
labs = [t[:3] for t in butterfly]
print("Data from butterfly:", np.unique(labs, return_counts=True))

# Check metadata table
table = pd.read_csv(metadata)

# Find and copy the ones that have no MD comment
print("----------------------------")
print("Find and copy the ones that have no MD comment")
md1 = table["Comments first medical doctor (MD1)"].values
md2 = table["MD2"].values
for i in range(len(table)):
    if (pd.isnull(md1[i]) and pd.isnull(md2[i])
        ) or (md1[i] == "Video not found" and pd.isnull(md2[i])):
        if not pd.isnull(table.iloc[i]["Current location"]):
            location = table.iloc[i]["Current location"].lower()
            if location.startswith("data/"):
                location = location[5:]
            if "not" in location:
                continue
            print(table.iloc[i]["Filename"])
            location = table.iloc[i]["Current location"].lower()
            if location.startswith("data/"):
                location = location[5:]
            for ending in ["", ".jpeg", ".png", ".jpg", ".mp4", ".JPG"]:
                try:
                    if out is not None:
                        shutil.copy(
                            os.path.join(
                                base, location,
                                table.iloc[i]["Filename"] + ending
                            ), out
                        )
                        print("copied successfully")
                    if ending != "":
                        print(
                            table.iloc[i]["Filename"], "worked with ending",
                            ending
                        )
                    break
                except FileNotFoundError:
                    if ending == ".JPG":
                        print(
                            os.path.join(
                                base, location, table.iloc[i]["Filename"]
                            )
                        )
                    pass

# Find which filenames appear in the sheet but not in the specified folder
print("-------------------------")
print(
    "Find which filenames appear in the sheet but not in the specified folder"
)

possible_endings = [
    "", ".jpeg", ".png", ".jpg", ".mp4", ".JPG", ".mpeg", ".avi", ".gif",
    ".mov"
]
for i in range(len(table)):
    fn = table.iloc[i]["Filename"]
    location = table.iloc[i]["Current location"].lower()
    if pd.isnull(location) or 'data_with_artifacts' in location:
        continue
    if location.startswith("data/"):
        location = location[5:]

    path1 = os.path.join(base, location, fn)
    path2 = ".".join(path1.split(".")[:-1]) + ".mp4"
    missing = True
    for ending in possible_endings:
        if os.path.exists(path1 + ending):
            missing = False
    if missing:
        if not ("not" in location or "Butterfly" in fn):
            # if not os.path.exists(os.path.join(base, location, fn + ".png")):
            print(fn, "missing at", location)

# Find which filenames appear in folder but not in sheet
print("----------------------")
print("Find which filenames appear in folder but not in sheet")

folders = [
    "pocus_images/convex", "pocus_images/linear", "pocus_videos/linear",
    "pocus_videos/convex"
]

filenames_in_table = table["Filename"].values

for fold in folders:
    for fn in os.listdir(os.path.join(base, fold)):
        if not (fn.startswith(".") or "Butterfly" in fn):
            fn_without = fn.split(".")[0]
            if fn_without not in filenames_in_table:
                print(fold, fn)
