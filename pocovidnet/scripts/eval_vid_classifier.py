import argparse
import json
import os
import pickle
import numpy as np
from pocovidnet.evaluate_genesis import GenesisEvaluator
from pocovidnet.evaluate_video import VideoEvaluator
from tensorflow.keras import backend as K
from pocovidnet.videoto3d import Videoto3D


def main():
    parser = argparse.ArgumentParser(description='Evaluate genesis and cam')
    parser.add_argument('--json', type=str, default="../data/cross_val.json")
    parser.add_argument(
        '--genesis_weights', type=str, default='video_genesis_lr1e4'
    )
    parser.add_argument(
        '--frame_model_weights', type=str, default='trained_models_cam'
    )
    parser.add_argument(
        '--frame_model_id', type=str, default='vgg_cam'
    )
    parser.add_argument(
        '--videos', type=str, default='../data/pocus_videos/convex'
    )
    parser.add_argument(
        '--output_dir', type=str, default='evaluation_outputs.dat'
    )
    args = parser.parse_args()

    K.clear_session()

    print("---------------------------------")
    print("WARNING: THIS SCRIPT MUST BE RUN ON A GPU")
    print("---------------------------------")

    with open(args.json, "r") as infile:
        cross_val_split = json.load(infile)

    VIDEO_DIR = args.videos
    all_genesis_preds = []
    all_frame_preds = []
    for i in range(5):
        gen_eval = GenesisEvaluator(
            weights_dir=args.genesis_weights, ensemble=False, split=i
        )
        K.set_image_data_format("channels_last")
        normal_eval = VideoEvaluator(
            weights_dir=args.frame_model_weights,
            ensemble=False,
            split=i,
            model_id=args.frame_model_id,
            num_classes=4
        )
        files = cross_val_split[str(i)]["test"][0]
        # print(files)
        for f in files:
            print("evaluate", f)
            # TEST if the video is working
            vid3d = Videoto3D("", 64, 64, 5, 5)
            vid3d.max_vid = {"cov": 20, "pne": 20, "reg": 20}
            X_test, _, fn = vid3d.video3d(
                [os.path.join(VIDEO_DIR, f)], ["cov"]
            )
            if len(np.unique(fn)) != 1:
                print("ERROR: WRONG FILE!")
                print(fn)
                print(X_test.shape)
                continue
            # run genesis model
            K.set_image_data_format("channels_first")
            preds = gen_eval(os.path.join(VIDEO_DIR, f))
            vid_pred_genesis = np.argmax(np.mean(preds, axis=(0, 1)))
            all_genesis_preds.append(preds)
            # run cam model
            K.set_image_data_format("channels_last")
            preds_framebased = normal_eval(os.path.join(VIDEO_DIR, f))
            frame_pred = np.argmax(np.mean(preds_framebased, axis=0))
            all_frame_preds.append(preds_framebased)
            print(preds.shape, preds_framebased.shape)
            print(
                "genesis pred", vid_pred_genesis, "frame based pred",
                frame_pred
            )
            print("-------------")
    with open(args.output_dir, "wb") as outfile:
        pickle.dump((all_genesis_preds, all_frame_preds), outfile)


if __name__ == '__main__':
    main()
