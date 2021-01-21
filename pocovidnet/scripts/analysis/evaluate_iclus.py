import argparse
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib
import json
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

        bottom, top, left, right = tuple(self.crop_inds)
        cap = cv2.VideoCapture(video_path)
        images = []
        count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if (ret != 1):
                break
            img_processed = self.preprocess(frame[bottom:top, left:right])[0]
            images.append(img_processed)
            count += 1
        cap.release()
        return np.array(images)


# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    '-d',
    '--data_dir',
    default="../../data/ICLUS",
    help='Path to input dataset'
)
ap.add_argument(
    '-m',
    '--model_dir',
    default="../models/oct_base",
    help='Path to model weights'
)
ap.add_argument(
    '-o', '--output_dir', default="iclus_preds", help='Path to save heatmaps'
)
ap.add_argument('--m_id', type=str, default='vgg_base')
ap.add_argument('--uncertain', type=bool, default=True)

args = ap.parse_args()

if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

# initialize model
evaluator = IclusEvaluator(
    ensemble=True,
    weights_dir=args.model_dir,
    model_id=args.m_id,
    num_classes=4
)
if args.uncertain:
    evaluator.make_dropout_evaluator()

# define output path
out_iclus_data = args.output_dir

# set cropping

with open(os.path.join(args.data_dir, 'ICLUS_cropping.json'), "r") as infile:
    frame_cut = json.load(infile)

for subfolder in os.listdir(args.data_dir):
    if "linear" in subfolder.lower(
    ) or subfolder.startswith(".") or os.path.isfile(
        os.path.join(args.data_dir, subfolder)
    ):
        continue
    for vid in os.listdir(os.path.join(args.data_dir, subfolder)):
        vid_id = vid.split(".")[0]
        if vid.startswith(".") or os.path.exists(
            os.path.join(out_iclus_data, "pred_" + vid_id + ".npy")
        ):
            print("already done", vid)
            continue
        crop = frame_cut[vid_id]
        print("process next file ", vid_id, crop)

        # set crop in evaluator
        evaluator.crop_inds = crop

        # Uncertainty:
        if args.uncertain:
            evaluator.image_arr = evaluator.read_video(
                os.path.join(args.data_dir, subfolder, vid)
            )
            uncertainties = np.zeros((2, 5, len(evaluator.image_arr)))
            preds = np.zeros((2, 5, len(evaluator.image_arr)))
            for j, method in enumerate(["epistemic", "aleatoric"]):
                for model_idx in range(5):
                    for img_idx, img in enumerate(evaluator.image_arr):
                        conf, pred = evaluator.get_uncertainty(
                            model_idx, img, method="epistemic"
                        )
                        # print(
                        #     method, model_idx, "img", img_idx, "conf", conf,
                        #     pred
                        # )
                        uncertainties[j, model_idx, img_idx] = conf
                        preds[j, model_idx, img_idx] = pred
            # save uncertainty estimates
            np.save(
                os.path.join(out_iclus_data, "conf_" + vid_id + ".npy"),
                uncertainties
            )
        else:
            preds = evaluator(os.path.join(args.data_dir, subfolder, vid))

        np.save(os.path.join(out_iclus_data, "pred_" + vid_id + ".npy"), preds)
        plt.imshow(evaluator.image_arr[10])
        plt.savefig(
            os.path.join(out_iclus_data, "pred_" + vid_id + "example_img.png")
        )
        print("saved predictions")
        pred_plot(preds, os.path.join(out_iclus_data, "pred_" + vid_id))
        print("saved plot")
