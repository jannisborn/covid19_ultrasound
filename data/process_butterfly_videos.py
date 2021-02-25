from pocovidnet.utils_butterfly_data import (
    get_processing_info, get_paths, label_to_dir
)
import os
import cv2
import numpy as np

import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-data', type=str, default=os.path.join("butterfly", "Published ")
    )
    parser.add_argument('-out', type=str, default="pocus_videos/convex")
    parser.add_argument('-json', type=str, default="data_from_butterfly.json")
    args = parser.parse_args()

    butterfly_dir = args.data
    out_dir = args.out

    actual_names, labels = get_paths(args.json)
    # manually add the ones which I know are in the data
    files_to_process, labs_to_process = get_processing_info(
        butterfly_dir, actual_names, labels
    )

    del_upper = 100
    for i in range(len(files_to_process)):
        vid_arr = []
        fp = files_to_process[i]
        fn = fp.split(os.sep)[-1]
        cap = cv2.VideoCapture(fp)  # capturing the video from the given path
        # frame rate
        n_frames = cap.get(7)
        frameRate = cap.get(5)
        out_path = os.path.join(
            out_dir,
            label_to_dir(labs_to_process[i]).split(os.sep)[1][:3]
        )
        print(out_path)
        print(
            "PROCESS", fn, labs_to_process[i], "framerate", int(cap.get(5)),
            "width", cap.get(3), "height", cap.get(4), "number frames:",
            cap.get(7)
        )
        full_save_path = out_path + "_Butterfly_" + fn.split(".")[0] + ".avi"
        if os.path.exists(full_save_path):
            print("already done, ", full_save_path)
            continue

        (out_width, out_height) = (int(cap.get(3)), int(cap.get(4)))

        nr_selected = 0
        while cap.isOpened():
            frameId = cap.get(1)  # current frame number
            ret, frame = cap.read()
            if not ret:
                break

            vid_arr.append(frame)
        cap.release()
        vid_arr = np.asarray(vid_arr)
        # SAVE VIDEO
        if len(vid_arr) > 5:
            curr_size = vid_arr.shape[1:3]
            print("output video size", curr_size)
            fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
            writer = cv2.VideoWriter(
                full_save_path, fourcc, 20.0, (out_width, out_height)
            )
            for x in vid_arr:
                writer.write(x.astype("uint8"))
            writer.release()
            # # If OpenCV does not work, install skvideo and try skvideo.io
            # io.vwrite(
            #     out_path + "_Butterfly_" + fn.split(".")[0] + ".mpeg",
            #     vid_arr,
            #     outputdict={"-vcodec": "mpeg2video"}
            # )
            print("DONE", vid_arr.shape)
        else:
            print("Invalid video, could not read frames:", fn)
