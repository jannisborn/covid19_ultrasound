import cv2
import numpy as np
import os
from pocovidnet.evaluate_covid19 import Evaluator
from pocovidnet.grad_cam import GradCAM
from pocovidnet.cam import get_class_activation_map


class VideoEvaluator(Evaluator):
    """
    Predict class probabilities for a video and return the CAMS for the most
    decisive frames
    """

    def __init__(self, ensemble=True, split=None, model_id=None):
        Evaluator.__init__(
            self, ensemble=ensemble, split=split, model_id=model_id
        )

    def __call__(self, video_path, return_cams=5):
        """Performs a forward pass through the restored model

        Arguments:
            video_path: str -- file path to a video to process. Possibly types
                        are mp4, gif, mpeg
            return_cams: int -- number of frames to return with activation maps
                        overlayed. If zero, only the predictions will be
                        returned. Always selects the frames with highest
                        probability for the predicted class

        Returns:
        	cams: if return_cams>0, images with overlay are returned as a
                    np.array {number models} x {return_cams} x 224 x 224 x 3
            mean_preds: np array of shape {video length} x {number classes}.
                        Contains class probabilities per frame
        """

        image_arr = self.read_video(video_path)
        predictions = np.stack(
            [model.predict(image_arr) for model in self.models]
        )

        mean_preds = np.mean(predictions, axis=0, keepdims=False)
        class_idx = np.argmax(np.mean(np.array(mean_preds), axis=0))

        if return_cams > 0:
            best_frames = self.important_frames(
                mean_preds, class_idx, n_return=return_cams
            )

            print("processing cams ....")
            print(
                "class preds:", np.mean(mean_preds, axis=0), " - using class",
                class_idx
            )
            cams = np.zeros((len(self.models), return_cams, 224, 224, 3))
            for i, model in enumerate(self.models):
                for j, b_frame in enumerate(best_frames):
                    if "cam" in self.model_id:
                        cams[i, j] = get_class_activation_map(
                            model, image_arr[b_frame], class_idx
                        )
                    else:
                        # run grad cam for other models
                        gradcam = GradCAM()
                        cams[i, j] = (
                            gradcam.explain(
                                image_arr[b_frame],
                                model,
                                class_idx,
                                return_map=False
                            )
                        )
            return cams, mean_preds
        else:
            return mean_preds

    def read_video(self, video_path):
        """
        Read in video and resize frames
        Arguments:
            video_path: str -- file path to video file
        Returns:
            3D array of frames (size 224x224x3)
        """
        assert os.path.exists(video_path), "video file not found"

        cap = cv2.VideoCapture(video_path)
        images = []
        while cap.isOpened():
            ret, frame = cap.read()
            if (ret != True):
                break
            img_processed = self.preprocess(frame)[0]
            images.append(img_processed)
        cap.release()
        return np.array(images)

    def important_frames(self, preds, predicted_class, n_return=5):
        """
        Compute most important frames
        Arguments:
            preds: 2D array with class predictions per frame
            predicted_class: int
            n_return: int - how many to return
        Returns:
            integer array of indices of most important frames (sorted)
        """
        preds_arr = np.array(preds)
        frame_scores = preds_arr[:, predicted_class]
        best_frames = np.argsort(frame_scores)[-n_return:]
        return best_frames
