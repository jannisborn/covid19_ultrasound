import cv2
import numpy as np
import os
from pocovidnet.evaluate_covid19 import Evaluator
from pocovidnet.grad_cam import GradCAM
from pocovidnet.cam import get_class_activation_map
from pocovidnet.utils_uncertainty import (
    overlay_precision_gauge, confidence_to_precision, confidence_bar
)


class VideoEvaluator(Evaluator):
    """
    Predict class probabilities for a video and return the CAMS for the most
    decisive frames
    """

    def __init__(
        self,
        weights_dir="trained_models",
        ensemble=True,
        split=None,
        model_id=None,
        num_classes=3
    ):
        Evaluator.__init__(
            self,
            weights_dir=weights_dir,
            ensemble=ensemble,
            split=split,
            model_id=model_id,
            num_classes=num_classes
        )

        self.weights_dir = weights_dir
        self.num_classes = num_classes

    def __call__(self, video_path):
        """Performs a forward pass through the restored model

        Arguments:
            video_path: str -- file path to a video to process. Possibly types
                        are mp4, gif, mpeg
        Returns:
            mean_preds: np array of shape {video length} x {number classes}.
                        Contains class probabilities per frame
        """

        self.image_arr = self.read_video(video_path)
        self.predictions = np.stack(
            [model.predict(self.image_arr) for model in self.models]
        )
        # output probabilities instead of log probs
        if np.any(self.predictions < 0):
            self.predictions = np.exp(self.predictions)
        # Take average over all frames
        mean_preds = np.mean(self.predictions, axis=0, keepdims=False)
        return mean_preds

    def cam_important_frames(
        self,
        threshold=0.75,
        nr_cams=None,
        zeroing=0.65,
        save_video_path=None,
        uncertainty_method=None,
        cam_layer_name="block5_conv3",
        cam_output_size=(224, 224)
    ):
        """
        Compute CAMs on most decisive frames and save as video
        Arguments:
            EITHER treshold or nr_cams will be selected
            threshold: float between 0 and 1, minimum prediction probability
                        to select a frame
            nr_cams: int - if not None then the number of frames to take
            zeroing: for grad cam
            save_video_path: output path (without ending!)
            uncertainty_method: None if don't wont to show uncertainty,
                otherwise one of 'epistemic' or 'aleatoric
        """
        if uncertainty_method is not None:
            # To display the gauge, we need a 1000 x 1000 image
            cam_output_size = (1000, 1000)
        if uncertainty_method == 'epistemic':
            self.make_dropout_evaluator()

        # Unpack target dimensions
        cam_dim_x, cam_dim_y = cam_output_size

        # Get predictions
        mean_preds = np.mean(self.predictions, axis=0, keepdims=False)

        # Get class index
        class_idx = np.argmax(np.mean(np.array(mean_preds), axis=0))

        # Get most important frames (the ones above threshold) to display
        if nr_cams is not None:
            best_frames = np.argsort(mean_preds[:, class_idx])[-nr_cams:]
        else:
            best_frames = np.where(mean_preds[:, class_idx] > threshold)[0]

        print(
            "pred class:", class_idx, "\nframes above threshold", best_frames
        )

        # Map to [0,255]
        copied_arr = np.zeros((len(self.image_arr), cam_dim_x, cam_dim_y, 3))

        # Resize images
        for idx in range(copied_arr.shape[0]):
            copied_arr[idx, :, :, :] = (
                cv2.resize(self.image_arr[idx], (cam_dim_x, cam_dim_y)) * 255
            ).astype(int)

        # Create placeholder for CAMs
        cams = np.zeros((len(best_frames), cam_dim_x, cam_dim_y, 3))

        if uncertainty_method is not None:
            precision_best_frames = list()

        # MAIN PART: GET CAMS AND UNCERTAINTIES
        for j, b_frame in enumerate(best_frames):
            # get highest prob model for this frame
            model_idx = np.argmax(
                self.predictions[:, b_frame, class_idx], axis=0
            )

            # compute cam
            in_img = self.image_arr[b_frame]
            cams[j] = self.compute_cam(
                in_img,
                model_idx,
                class_idx,
                zeroing,
                layer_name=cam_layer_name,
                out_size=cam_output_size
            )

            # compute uncertainty
            if uncertainty_method is not None:
                precision = self.get_uncertainty(
                    model_idx, in_img, runs=10, method=uncertainty_method
                )
                precision_best_frames.append(precision)

        # Output
        if save_video_path is None:
            # output raw cams
            return cams
        else:
            # save image or video
            for j in range(len(best_frames)):
                copied_arr[best_frames[j]] = cams[j]

                # Add uncertainty overlay if desired
                if uncertainty_method is not None:
                    copied_arr[best_frames[j]] = overlay_precision_gauge(
                        copied_arr[best_frames[j]], precision_best_frames[j][0]
                    )
            # image processing
            if len(copied_arr) == 1:
                cv2.imwrite(save_video_path + ".png", copied_arr[0])
                return save_video_path + ".png"
            # or video processing
            else:
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                writer = cv2.VideoWriter(
                    save_video_path + '.avi', fourcc, 10.0, cam_output_size
                )
                for x in copied_arr:
                    writer.write(x.astype("uint8"))
                writer.release()
                return save_video_path + ".avi"

    def compute_cam(
        self,
        in_img,
        model_idx,
        class_idx,
        zeroing,
        layer_name="block5_conv3",
        out_size=(224, 224)
    ):
        if "cam" in self.model_id:
            in_img = np.expand_dims(in_img, 0)
            cam = get_class_activation_map(
                self.models[model_idx],
                in_img,
                class_idx,
                zeroing=zeroing,
                size=out_size
            ).astype(int)
        else:
            # run grad cam for other models
            gradcam = GradCAM()
            cam = gradcam.explain(
                in_img,
                self.models[model_idx],
                class_idx,
                return_map=False,
                layer_name=layer_name,
                zeroing=zeroing,
                image_weight=1,
                heatmap_weight=0.25,
                size=out_size
            )
        return cam

    def make_dropout_evaluator(self):
        self.dropout_evaluator = Evaluator(
            weights_dir=self.weights_dir,
            ensemble=self.ensemble,
            split=self.split,
            model_id=self.model_id,
            num_classes=self.num_classes,
            mc_dropout=True
        )

    def read_video(self, video_path):
        assert os.path.exists(video_path), "video file not found"

        cap = cv2.VideoCapture(video_path)
        images = []
        while cap.isOpened():
            ret, frame = cap.read()
            if (ret != 1):
                break
            img_processed = self.preprocess(frame)[0]
            images.append(img_processed)
        cap.release()
        return np.array(images)

    def important_frames(self, preds, predicted_class, n_return=5):
        preds_arr = np.array(preds)
        frame_scores = preds_arr[:, predicted_class]
        best_frames = np.argsort(frame_scores)[-n_return:]
        return best_frames

    def get_uncertainty(self, model_idx, image, runs=10, method='epistemic'):
        """
        Computes the precision of predictions of model given image.
        method can either
            'epistemic' (dropout during inference)
            'aleatoric' (test time augmentation)
        """

        if method == 'epistemic':
            model = self.dropout_evaluator.models[model_idx]
        elif method == 'aleatoric':
            model = self.models[model_idx]
            image = np.squeeze(
                next(self.augmentor.flow(np.expand_dims(image, 0)))
            )
        else:
            print(
                f"invalid method '{method}', must be 'epistemic' or 'aleatoric'"
            )
            return

        # MAIN STEP: feed through model and compute logits {runs} times
        # raw_logits = np.zeros((runs, self.num_classes))
        # for idx in range(runs):
        #     raw_logits[idx, :] = model(image.astype(np.float32))
        input_images = np.asarray(
            [image.astype(np.float32) for _ in range(runs)]
        )
        raw_logits = model(input_images)

        # compute first two moments of predictions
        logits_mean = np.mean(raw_logits, axis=0)
        logits_stds = np.std(raw_logits, axis=0)

        # get classification result
        pred_idx = np.argmax(logits_mean)

        precision = confidence_to_precision(logits_stds[pred_idx])

        return precision, pred_idx
