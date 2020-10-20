import os
import argparse
import numpy as np
import shutil
import json

# NOTE: To use the default parameters, execute this from the main directory of
# the package.

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    "-d",
    "--data_dir",
    type=str,
    default="../data/image_dataset",
    help=("Raw data path. Expects 3 or 4 subfolders with classes")
)
ap.add_argument(
    "-o",
    "--output_dir",
    type=str,
    default="../data/cross_validation/",
    help=("Output path where images for cross validation will be stored.")
)
ap.add_argument(
    "-v",
    "--video_dir",
    type=str,
    default="../data/pocus_videos/convex/",
    help=("Path where the videos of the database are stored")
)
ap.add_argument(
    "-s",
    "--splits",
    type=int,
    default=5,
    help="Number of folds for cross validation"
)
args = vars(ap.parse_args())

NUM_FOLDS = args['splits']
DATA_DIR = args['data_dir']
OUTPUT_DIR = args['output_dir']

# MAKE DIRECTORIES
for split_ind in range(NUM_FOLDS):
    # make directory for this split
    split_path = os.path.join(OUTPUT_DIR, 'split' + str(split_ind))
    if not os.path.exists(split_path):
        os.makedirs(split_path)

# MAKE SPLIT
copy_dict = {}
for classe in os.listdir(DATA_DIR):
    if classe[0] == ".":
        continue
    # make directories:
    for split_ind in range(NUM_FOLDS):
        mod_path = os.path.join(OUTPUT_DIR, 'split' + str(split_ind), classe)
        if not os.path.exists(mod_path):
            os.makedirs(mod_path)

    uni_videos = []
    uni_images = []
    for in_file in os.listdir(os.path.join(DATA_DIR, classe)):
        if in_file[0] == ".":
            continue
        if len(in_file.split(".")) == 3:
            # this is a video
            uni_videos.append(in_file.split(".")[0])
        else:
            # this is an image
            uni_images.append(in_file.split(".")[0])
    # construct dict of file to fold mapping
    inner_dict = {}
    # consider images and videos separately
    for k, uni in enumerate([uni_videos, uni_images]):
        unique_files = np.unique(uni)
        # s is number of files in one split
        s = len(unique_files) // NUM_FOLDS
        for i in range(NUM_FOLDS):
            for f in unique_files[i * s:(i + 1) * s]:
                inner_dict[f] = i
        # distribute the rest randomly
        for f in unique_files[NUM_FOLDS * s:]:
            inner_dict[f] = np.random.choice(np.arange(5))

    copy_dict[classe] = inner_dict
    for in_file in os.listdir(os.path.join(DATA_DIR, classe)):
        fold_to_put = inner_dict[in_file.split(".")[0]]
        split_path = os.path.join(
            OUTPUT_DIR, 'split' + str(fold_to_put), classe
        )
        # print(os.path.join(DATA_DIR, classe, file), split_path)
        shutil.copy(os.path.join(DATA_DIR, classe, in_file), split_path)


def check_crossval(cross_val_directory="../data/cross_validation"):
    """
    Test method to check a cross validation split (prints number of unique f)
    """
    check = cross_val_directory
    file_list = []
    for folder in os.listdir(check):
        if folder[0] == ".":
            continue
        for classe in os.listdir(os.path.join(check, folder)):
            if classe[0] == "." or classe[0] == "u":
                continue
            uni = []
            is_image = 0
            for file in os.listdir(os.path.join(check, folder, classe)):
                if file[0] == ".":
                    continue
                if len(file.split(".")) == 2:
                    is_image += 1
                file_list.append(file)
                uni.append(file.split(".")[0])
            print(folder, classe, len(np.unique(uni)), len(uni), is_image)
    if len(file_list) != len(np.unique(file_list)):
        print("PROBLEM: FILES THAT APPEAR TWICE")
        # print(len(file_list), len(np.unique(file_list)))
        uni, counts = np.unique(file_list, return_counts=True)
        for i in range(len(counts)):
            if counts[i] > 1:
                print(uni[i])
    else:
        print("Fine, every file is unique")


# check whether all files are unique
check_crossval()

# MAKE VIDEO CROSS VAL FILE --> corresponds to json cross val

check = OUTPUT_DIR
videos_dir = args["video_dir"]

file_list = []
video_cross_val = {}
for split in range(5):
    train_test_dict = {"test": [[], []], "train": [[], []]}
    for folder in os.listdir(check):
        if folder[0] == ".":
            continue
        for classe in os.listdir(os.path.join(check, folder)):
            if classe[0] == "." or classe[0] == "u":
                continue
            uni = []
            for file in os.listdir(os.path.join(check, folder, classe)):
                if file[0] == "." or len(file.split(".")) == 2:
                    continue
                parts = file.split(".")
                if not os.path.exists(
                    os.path.
                    join(videos_dir, parts[0] + "." + parts[1].split("_")[0])
                ):
                    butterfly_name = parts[0][:3] + "_Butterfly_" + parts[0][
                        4:] + ".avi"
                    if not os.path.exists(
                        os.path.join(videos_dir, butterfly_name)
                    ):
                        print("green dots in video or aibronch", file)
                        continue
                    uni.append(butterfly_name)
                else:
                    uni.append(parts[0] + "." + parts[1].split("_")[0])
            uni_files_in_split = np.unique(uni)
            uni_labels = [vid[:3].lower() for vid in uni_files_in_split]

            if folder[-1] == str(split):
                train_test_dict["test"][0].extend(uni_files_in_split)
                train_test_dict["test"][1].extend(uni_labels)
            else:
                train_test_dict["train"][0].extend(uni_files_in_split)
                train_test_dict["train"][1].extend(uni_labels)
    video_cross_val[split] = train_test_dict

with open(os.path.join("..", "data", "cross_val.json"), "w") as outfile:
    json.dump(video_cross_val, outfile)

this_class = {"cov": "covid", "pne": "pneumonia", "reg": "regular"}
for i in range(5):
    all_labels = []
    files, labs = video_cross_val[i]["test"]
    for j in range(len(files)):
        assert os.path.exists(
            os.path.join(
                OUTPUT_DIR, "split" + str(i), this_class[labs[j]],
                files[j] + "_frame0.jpg"
            )
        ), files[j] + "  in  " + str(i)
