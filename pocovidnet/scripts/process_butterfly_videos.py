from pocovidnet.utils_butterfly_data import (
    get_processing_info, get_paths, label_to_dir
)
import os
import cv2
import numpy as np

import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-data', type=str, default="butterfly")
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
        if os.path.exists(out_path + "_" + fn.split(".")[0] + ".mpeg"):
            print(
                "already done, ", out_path + "_" + fn.split(".")[0] + ".mpeg"
            )
            continue

        nr_selected = 0
        while cap.isOpened():
            frameId = cap.get(1)  # current frame number
            ret, frame = cap.read()
            if not ret:
                break

            frame = np.asarray(frame).astype(int)
            # crop
            width_border = int(cap.get(3) * 0.15)
            width_box = int(cap.get(3)) - 2 * width_border
            if width_box + del_upper > cap.get(4):
                width_box = int(cap.get(4) - del_upper)
                width_border = int(cap.get(3) / 2 - width_box / 2)
            frame = frame[del_upper:width_box + del_upper,
                          width_border:width_box + width_border]

            # detect green point
            green_point = frame[:, :, 1] - frame[:, :, 0]
            # get first frame for green point deletion:
            if frameId == 0:
                frame_start = green_point
            # skip the green moving points
            if np.any((green_point - frame_start) > 100):
                # plt.imshow(green_point)
                # plt.show()
                print("VID WITH GREEN DOT")
                break
            # delete blue symbol
            blue_symbol = np.where(green_point < -50)
            frame[blue_symbol] = frame[0, 0]
            # delete green symbol
            if np.any(green_point > 220):
                green_symbol = np.where(green_point > 50)
                frame[green_symbol] = frame[0, 0]
            # resize
            frame = np.asarray(frame).astype(np.uint8)
            # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            # frame = cv2.resize(frame, (240, 240))
            # if frameId == 0:
            #     plt.imshow(frame)
            #     plt.show()
            vid_arr.append(frame)
        cap.release()
        vid_arr = np.asarray(vid_arr)
        # SAVE VIDEO
        if len(vid_arr) > 5:
            curr_size = vid_arr.shape[1:3]
            print("output video size", curr_size)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            writer = cv2.VideoWriter(
                out_path + "_Butterfly_" + fn.split(".")[0] + ".avi", fourcc,
                20.0, tuple(curr_size)
            )
            for x in vid_arr:
                writer.write(x.astype("uint8"))
            writer.release()
            # io.vwrite(
            #     out_path + "_Butterfly_" + fn.split(".")[0] + ".mpeg",
            #     vid_arr,
            #     outputdict={"-vcodec": "mpeg2video"}
            # )
            print("DONE", vid_arr.shape)
        else:
            print("GREEN DOT:", fn)
