import pandas as ps
import numpy as np
import cv2  # for capturing videos
import os
import shutil
import argparse

TAKE_CLASSES = ["covid", "pneumonia", "regular"]  # can add viral
TAKE_MODE = ["convex"]  # can add linear


def label_to_dir(lab):
    if lab == "Cov":
        label = "covid"
    elif lab == "Pne" or lab == "pne":
        label = "pneumonia"
    elif lab == "Reg":
        label = "regular"
    elif lab == "Vir":
        label = "viral"
    else:
        raise ValueError("Wrong label! " + lab)
    return label


if __name__ == "__main__":
    # ARGUMENTS
    parser = argparse.ArgumentParser()
    parser.add_argument('-imgs', type=str, default="../data/pocus_images")
    parser.add_argument('-out', type=str, default="../data/image_dataset")
    parser.add_argument('-vids', type=str, default="../data/pocus_videos")
    parser.add_argument(
        '-fr',
        help="framerate - at how much Hz to sample",
        type=int,
        default=3
    )
    parser.add_argument(
        '-max',
        help="maximum of frames to sample from one video",
        type=int,
        default=30
    )
    args = parser.parse_args()

    FRAMERATE = args.fr
    # saves automatically <FRAMERATE> frames per second
    MAX_FRAMES = args.max
    POCUS_IMAGE_DIR = args.imgs
    POCUS_VIDEO_DIR = args.vids
    out_image_dir = args.out

    if not os.path.exists(out_image_dir):
        os.makedirs(out_image_dir)
    for mod in TAKE_CLASSES:
        if not os.path.exists(os.path.join(out_image_dir, mod)):
            os.makedirs(os.path.join(out_image_dir, mod))

    # copy all images from pocus_images
    for mode in TAKE_MODE:
        for fp in os.listdir(os.path.join(POCUS_IMAGE_DIR, mode)):
            if fp[-3:] in ["png", "jpg", "peg", "JPG", "PNG"]:
                label_dir = label_to_dir(fp[:3])
                if label_dir in TAKE_CLASSES:
                    shutil.copy(
                        os.path.join(POCUS_IMAGE_DIR, mode, fp),
                        os.path.join(out_image_dir, label_dir)
                    )

    # process all videos
    for mode in TAKE_MODE:
        vid_files = os.listdir(os.path.join(POCUS_VIDEO_DIR, mode))
        for i in range(len(vid_files)):

            # skip non video files
            if vid_files[i][-3:].lower() not in [
                "peg", "gif", "mp4", "m4v", "avi", "mov"
            ]:
                continue

            # define video path
            video_path = os.path.join(POCUS_VIDEO_DIR, mode, vid_files[i])
            # determine label
            label = label_to_dir(vid_files[i][:3])
            if label not in TAKE_CLASSES:
                continue
            # determine out path based on label
            out_path = os.path.join(out_image_dir, label)

            # read and write if video
            cap = cv2.VideoCapture(
                video_path
            )  # capturing the video from the given path
            frameRate = cap.get(5)  #frame rate
            # num_frames = cap.get(7)
            every_x_image = int(frameRate / FRAMERATE)
            print(
                vid_files[i], "framerate", cap.get(5), "width", cap.get(3),
                "height", cap.get(4), "number frames:", cap.get(7)
            )
            print("--> taking every ", every_x_image, "th image")
            x = 1
            nr_selected = 0
            while cap.isOpened() and nr_selected < MAX_FRAMES:
                frameId = cap.get(1)  #current frame number
                ret, frame = cap.read()
                if (ret != True):
                    break
                if (frameId % every_x_image == 0):
                    # storing the frames in a new folder named test_1
                    filename = os.path.join(
                        out_path, vid_files[i] + "_frame%d.jpg" % frameId
                    )
                    cv2.imwrite(filename, frame)
                    nr_selected += 1
            cap.release()
