import argparse
import json
import os
import pickle
import numpy as np
from pocovidnet.evaluate_genesis import GenesisEvaluator
from pocovidnet.evaluate_video import VideoEvaluator
from tensorflow.keras import backend as K


def main():
    parser = argparse.ArgumentParser(description='Evaluate genesis and cam')
    parser.add_argument(
        '--json', type=str, default="../data/video_input_data/cross_val.json"
    )
    parser.add_argument(
        '--genesis_weights', type=str, default='video_genesis_lr1e4'
    )
    parser.add_argument(
        '--cam_weights', type=str, default='trained_models_cam'
    )
    parser.add_argument(
        '--videos', type=str, default='../data/pocus_videos/convex'
    )
    args = parser.parse_args()

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
            weights_dir=args.cam_weights,
            ensemble=False,
            split=i,
            model_id="vgg_cam",
            num_classes=4
        )
        files = cross_val_split[str(i)]["test"][0]
        # print(files)
        for f in files:
            print("evaluate", f)
            # run genesis model
            preds = gen_eval(os.path.join(VIDEO_DIR, f))
            vid_pred_genesis = np.argmax(np.mean(preds, axis=(0, 1)))
            all_genesis_preds.append(preds)
            # run cam model
            preds_framebased = normal_eval(os.path.join(VIDEO_DIR, f))
            frame_pred = np.argmax(np.mean(preds_framebased, axis=(0, 1)))
            all_frame_preds.append(preds_framebased)
            print(preds.shape, preds_framebased.shape)
            print(
                "genesis pred", vid_pred_genesis, "frame based pred",
                frame_pred
            )
    with open("evaluation_outputs.dat", "wb") as outfile:
        pickle.dump((all_genesis_preds, all_frame_preds), outfile)


if __name__ == '__main__':
    main()
