# USAGE
# python sample_kaggle_dataset.py --kaggle chest_xray --output dataset/normal

# import the necessary packages
from imutils import paths
import argparse
import random
import shutil
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-k", "--kaggle", required=True,
	help="path to base directory of Kaggle X-ray dataset")
ap.add_argument("-o", "--output", required=True,
	help="path to directory where 'normal' images will be stored")
ap.add_argument("-s", "--sample", type=int, default=25,
	help="# of samples to pull from Kaggle dataset")
args = vars(ap.parse_args())

# grab all training image paths from the Kaggle X-ray dataset
basePath = os.path.sep.join([args["kaggle"], "train", "NORMAL"])
imagePaths = list(paths.list_images(args["kaggle"]))

# randomly sample the image paths
random.seed(42)
random.shuffle(imagePaths)
imagePaths = imagePaths[:args["sample"]]

# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
	# extract the filename from the image path and then construct the
	# path to the copied image file
	filename = imagePath.split(os.path.sep)[-1]
	outputPath = os.path.sep.join([args["output"], filename])

	# copy the image
	shutil.copy2(imagePath, outputPath)