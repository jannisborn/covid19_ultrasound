"""
Script to process the ultrasound videos from Butterfly:

"""
from pocovidnet.utils_butterfly_data import (
    makedirs, label_to_dir, get_paths, get_processing_info
)
import cv2
import numpy as np
import argparse
import os

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-data', type=str, default="butterfly")
    parser.add_argument('-out', type=str, default="image_dataset")
    parser.add_argument('-json', type=str, default="data_from_butterfly.json")
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

    del_upper = 100
    FRAMERATE = args.fr
    OUT_DIR = args.out
    MAX_FRAMES = args.max
    print("READ DATA FROM ", args.data)
    print("OUTPUT DATA IN ", args.out)
    print("SELECT FRAMES AT", args.fr, "Hz")
    print("SELECT MAXIMUM OF", args.max, "frames")

    actual_names, labels = get_paths(args.json)
    # manually add the ones which I know are in the data
    files_to_process, labs_to_process = get_processing_info(
        args.data, actual_names, labels
    )
    makedirs(OUT_DIR)

    # RUN - Iterate over videos
    for i in range(len(files_to_process)):  # 1,2): #
        fp = files_to_process[i]
        fn = fp.split(os.sep)[-1]
        cap = cv2.VideoCapture(fp)  # capturing the video from the given path
        # frame rate
        n_frames = cap.get(7)
        frameRate = cap.get(5)
        every_x_image = int(frameRate / FRAMERATE)
        out_path = os.path.join(OUT_DIR, label_to_dir(labs_to_process[i]))
        print(
            "PROCESS", fn, labs_to_process[i], "framerate", int(cap.get(5)),
            "width", cap.get(3), "height", cap.get(4), "number frames:",
            cap.get(7)
        )

        nr_selected = 0
        while cap.isOpened() and nr_selected < MAX_FRAMES:
            frameId = cap.get(1)  # current frame number
            ret, frame = cap.read()
            if not ret:
                break

            frame = np.asarray(frame).astype(int)
            # width_box = np.min(frame.shape[:2])
            # crop
            width_border = int(cap.get(3) * 0.15)
            width_box = int(cap.get(3)) - 2 * width_border
            frame = frame[del_upper:width_box +
                          del_upper, width_border:width_box + width_border]
            # frame = frame[width_border:width_box+width_border]
            # detect green point
            green_point = frame[:, :, 1] - frame[:, :, 0]
            # get first frame for green point deletion:
            if frameId == 0:
                frame_start = green_point
            # skip the green moving points
            if np.any((green_point - frame_start) > 100):
                continue
            # delete blue symbol
            blue_symbol = np.where(green_point < -50)
            frame[blue_symbol] = frame[0, 0]
            # delete green symbol
            if np.any(green_point > 220):
                green_symbol = np.where(green_point > 50)
                frame[green_symbol] = frame[0, 0]

            # SAVE
            if (frameId % every_x_image == 0):
                # storing the frames in a new folder named test_1
                filename = out_path + fn + "_frame%d.jpg" % frameId
                cv2.imwrite(filename, frame)
                nr_selected += 1
        print("Selected", nr_selected, "frames")
        cap.release()
