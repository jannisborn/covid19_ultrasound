import os
import argparse
import shutil

# NOTE: To use the default parameter, execute this from the main directory of
# the package.

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    "-i",
    "--imagenet_dir",
    type=str,
    default="../data/uniform_class_imagenet",
    help=("path to folder with imagenet data")
)
ap.add_argument(
    "-u",
    "--ultrasound_dir",
    type=str,
    default="../data/uniform_class_nerves",
    help=("Path to folder with ultrasound data (e.g. kaggle neck)")
)
ap.add_argument(
    "-o",
    "--output_dir",
    type=str,
    default="../data/cross_validation/",
    help=("Output path where images will be added to cross validation folds.")
)
ap.add_argument(
    "-s",
    "--splits",
    type=int,
    default=5,
    help="Number of folds for cross validation"
)
args = vars(ap.parse_args())

assert os.path.exists(args["imagenet_dir"]), "imagenet directory not found"
assert os.path.exists(args["ultrasound_dir"]), "US neck directory not found"

DIR_IMAGENET = args['imagenet_dir']
DIR_NERVES = args['ultrasound_dir']
NUM_FOLDS = args['splits']
OUTPUT_DIR = args['output_dir']

files_imagenet = os.listdir(DIR_IMAGENET)
files_nerves = os.listdir(DIR_NERVES)
nr_each_nerves = len(files_nerves) // NUM_FOLDS
nr_each_imagenet = len(files_imagenet) // NUM_FOLDS

for i in range(NUM_FOLDS):
    fold_dir = os.path.join(OUTPUT_DIR, "split" + str(i), "uninformative")
    if not os.path.exists(fold_dir):
        os.makedirs(fold_dir)
    copy_files_imagenet = files_imagenet[i * nr_each_imagenet:(i + 1) *
                                         nr_each_imagenet]
    copy_files_nerves = files_nerves[i * nr_each_nerves:(i + 1) *
                                     nr_each_nerves]
    #print(len(copy_files))
    for c in copy_files_imagenet:
        shutil.copy(os.path.join(DIR_IMAGENET, c), fold_dir)
    for c in copy_files_nerves:
        shutil.copy(os.path.join(DIR_NERVES, c), fold_dir)
