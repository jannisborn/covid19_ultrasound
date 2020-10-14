import argparse
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from pocovidnet.evaluate_video import VideoEvaluator


def pred_plot(preds, save_path):
    plt.figure(figsize=(15, 8))
    plt.plot(preds[:, 0], label="covid")
    plt.plot(preds[:, 1], label="pneu")
    plt.plot(preds[:, 2], label="healthy")
    plt.legend()
    plt.savefig(save_path + ".png")
    plt.show()


class IclusEvaluator(VideoEvaluator):

    def read_video(self, video_path):
        assert os.path.exists(video_path), "video file not found"

        cap = cv2.VideoCapture(video_path)
        images = []
        count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if (ret != 1) or count > 3:  #  TODO
                break
            img_processed = self.preprocess(frame[80:550, 470:940])[0]
            images.append(img_processed)
            count += 1
        cap.release()
        return np.array(images)


# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    '-d', '--data_dir', default="../data/ICLUS", help='Path to input dataset'
)
ap.add_argument(
    '-m', '--model_dir', default="models/oct_base", help='Path to model weights'
)
ap.add_argument(
    '-o', '--output_dir', default="results_oct/iclus", help='Path to save heatmaps'
)
ap.add_argument('--m_id', type=str, default='vgg_base')

args = ap.parse_args()

# initialize model
evaluator = IclusEvaluator(
    ensemble=True,
    weights_dir=args.model_dir,
    model_id=args.m_id,
    num_classes=4
)

# define output path
out_iclus_data = args.output_dir

for subfolder in os.listdir(args.data_dir):
    if "linear" in subfolder.lower() or subfolder.startswith("."):
        continue
    for vid in os.listdir(os.path.join(args.data_dir, subfolder)):
        vid_id = vid.split(".")[0]
        if vid.startswith(".") or os.path.exists(
            os.path.join(out_iclus_data, "cam_" + vid_id + ".npy")
        ):
            print("already done", vid)
            continue
        print("process next file ", vid)
        preds = evaluator(os.path.join(args.data_dir, subfolder, vid))
        np.save(os.path.join(out_iclus_data, "cam_" + vid_id + ".npy"), preds)
        plt.imshow(evaluator.image_arr[0])
        plt.savefig(
            os.path.join(out_iclus_data, "cam_" + vid_id + "example_img.png")
        )
        print("saved predictions")
        pred_plot(preds, os.path.join(out_iclus_data, "cam_" + vid_id))
        print("saved plot")
        # evaluator.cam_important_frames(GT_CLASS, save_video_path=os.path.join(out_iclus_data, "cam_"+vid_id))
