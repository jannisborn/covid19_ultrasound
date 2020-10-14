import shutil
import numpy as np
import pandas as pd
import os

base = "../../data/"
metadata = base + "dataset_metadata.csv"
out = "missing_MD_comments"

table = pd.read_csv(metadata)

# Find and copy the ones that have no MD comment
print("----------------------------")
print("Find and copy the ones that have no MD comment")
md1 = table["Comments first medical doctor (MD1)"].values
md2 = table["MD2"].values
for i in range(len(table)):
    if (pd.isnull(md1[i])
        and pd.isnull(md2[i])) or md1[i] == "Video not found":
        if not pd.isnull(table.iloc[i]["Current location"]):
            print(table.iloc[i]["Filename"])
            location = table.iloc[i]["Current location"].lower()
            if location.startswith("data/"):
                location = location[5:]
            if "bolzano" in table.iloc[i]["Filename"]:
                continue
            location = table.iloc[i]["Current location"].lower()
            if location.startswith("data/"):
                location = location[5:]
            for ending in ["", ".jpeg", ".png", ".jpg", ".mp4", ".JPG"]:
                try:
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
                                base, location,
                                table.iloc[i]["Filename"]
                            )
                        )
                    pass

# Find which filenames appear in the sheet but not in the specified folder
print("-------------------------")
print(
    "Find which filenames appear in the sheet but not in the specified folder"
)

for i in range(len(table)):
    fn = table.iloc[i]["Filename"]
    location = table.iloc[i]["Current location"].lower()
    if pd.isnull(location) or 'data_with_artifacts' in location:
        continue
    if location.startswith("data/"):
        location = location[5:]

    if not os.path.exists(os.path.join(base, location, fn)):
        if not ("not" in location or "Butterfly" in fn):
            # if not os.path.exists(os.path.join(base, location, fn + ".png")):
            print(fn, "missing at", location, "searching in", os.path.join(base, location, fn))

# Find which filenames appear in folder but not in sheet
print("----------------------")
print("Find which filenames appear in folder but not in sheet")

folders = [
    "pocus_images/convex", "pocus_images/linear",
    "pocus_videos/linear", "pocus_videos/convex"
]

filenames_in_table = table["Filename"].values

for fold in folders:
    for fn in os.listdir(os.path.join(base, fold)):
        if not (fn.startswith(".") or "Butterfly" in fn):
            if not (
                fn in filenames_in_table
                or fn.split(".")[0] in filenames_in_table
            ):
                print(fold, fn)
