import os
import argparse
import numpy as np
import shutil

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
    assert len(file_list) == len(np.unique(file_list))
    print(len(file_list))


# MAKE SPLIT OF APPROXIMATELY DIFFERENT SIZE
# split_test = [{} for _ in range(NUM_FOLDS)]
# num_scans_per_video = []
# for modality in ['covid', 'pneumonia', 'regular']:
#     p_vids = []
#     p_fn = []
#     for cov_data in os.listdir(os.path.join(DATA_DIR, modality)):
#         if cov_data[0] == '.':
#             continue
#         p_fn.append(cov_data)
#         p_vids.append(cov_data.split('.')[0])
#     vid_names, count1 = np.unique(p_vids, return_counts=True)
#     count = count1.copy()
#     name_list = [[v] for v in vid_names]

#     # summarize to number of split (always merge the ones with smallest count)
#     while len(count) > NUM_FOLDS:
#         arg_inds = np.argsort(count)
#         # merge smallest counts
#         count[arg_inds[0]] = count[arg_inds[0]] + count[arg_inds[1]]
#         count = np.delete(count, arg_inds[1])
#         # merge video names in smallest counts
#         name_list[arg_inds[0]].extend(name_list[arg_inds[1]])
#         del name_list[arg_inds[1]]
#     for i in range(len(name_list)):
#         print(name_list[i], count[i])
#         num_scans_per_video.append(count1[i])

#     # get filenames instead of video names
#     f_list = [[] for _ in range(NUM_FOLDS)]
#     for j in range(NUM_FOLDS):
#         # iterate over videos for this split
#         fn_list = []
#         for vid in name_list[j]:
#             fn_list.extend(np.array(p_fn)[np.array(p_vids) == vid])
#         f_list[j] = fn_list

#     # add to overall split list
#     for j in range(NUM_FOLDS):
#         split_test[j][modality] = f_list[j]

# # Copy data from into a new cross_val directory
# for split_ind in range(NUM_FOLDS):
#     # make directory for this split
#     split_path = os.path.join(OUTPUT_DIR, 'split' + str(split_ind))
#     if not os.path.exists(split_path):
#         os.makedirs(split_path)
#     # add each data type
#     for modality in split_test[split_ind].keys():
#         # make directory for each modality
#         mod_path = os.path.join(split_path, modality)
#         if not os.path.exists(mod_path):
#             os.makedirs(mod_path)
#         # copy all files
#         mod_split_files = split_test[split_ind][modality]
#         for fname in mod_split_files:
#             shutil.copy(os.path.join(DATA_DIR, modality, fname), mod_path)
