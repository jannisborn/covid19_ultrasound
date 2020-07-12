import cv2
import numpy as np
import os
from pocovidnet.evaluate_covid19 import Evaluator
from pocovidnet.grad_cam import GradCAM
from pocovidnet.cam import get_class_activation_map
from pocovidnet.uncertainty import get_uncertainty, overlay_precision_gauge


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

    def __call__(self, video_path):
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

        self.image_arr = self.read_video(video_path)
        self.predictions = np.stack(
            [model.predict(self.image_arr) for model in self.models]
        )

        mean_preds = np.mean(self.predictions, axis=0, keepdims=False)
        class_idx = np.argmax(np.mean(np.array(mean_preds), axis=0))

        return mean_preds

    def cam_important_frames(
        self,
        threshold=0.75,
        nr_cams=None,
        zeroing=0.65,
        save_video_path=None,
        uncertainty_method=None,
        cam_dims=(224,224)
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
        """
        if uncertainty_method is not None and cam_dims != (1000,1000):
            raise ValueError('When using uncertainty estimation, output size is restricted to (1000,1000).')

        # Unpack target dimensions
        cam_dim_x, cam_dim_y = cam_dims

        # Get predictions
        mean_preds = np.mean(self.predictions, axis=0, keepdims=False)
        
        # Get class index
        class_idx = np.argmax(np.mean(np.array(mean_preds), axis=0))
        
        # Get most important frames (the ones above threshold) to display
        if nr_cams is not None:
            best_frames = np.argsort(mean_preds[:, class_idx])[-nr_cams:]
        else:
            best_frames = np.where(mean_preds[:, class_idx] > threshold)[0]
        
        #best_frames = best_frames[:15]  #for debugging 
        return_cams = len(best_frames)

        print("pred class:", class_idx, "\nframes above threshold", best_frames)

        # Map to [0,255]
        copied_arr = (self.image_arr.copy() * 255).astype(int)
        copied_arr_hires = np.zeros((copied_arr.shape[0], cam_dim_x, cam_dim_y, 3))

        # Resize images
        for idx in range(copied_arr.shape[0]):
            copied_arr_hires[idx, :, :, :] = (cv2.resize(self.image_arr[idx], 
                                                        (cam_dim_x, cam_dim_y)) * 255).astype(int)
        
        # Create placeholder for CAMs
        cams = np.zeros((return_cams, cam_dim_x, cam_dim_y, 3))

        if uncertainty_method is not None:
            precision_best_frames = []

        # Loop over frames and get CAMs
        for j, b_frame in enumerate(best_frames):
            # get highest prob model for these frames
            model_idx = np.argmax(
                self.predictions[:, b_frame, class_idx], axis=0
            )
            take_model = self.models[model_idx]
            in_img = np.expand_dims(self.image_arr[b_frame], 0)

            if "cam" in self.model_id:
                
                # print(in_img.shape)
                
                cam = get_class_activation_map(
                    take_model, in_img, class_idx, zeroing=zeroing, size=(cam_dim_x, cam_dim_y)  #mg
                ).astype(int)

                cams[j] = cam
            else:
                # run grad cam for other models
                gradcam = GradCAM()
                cams[j] = gradcam.explain(
                    self.image_arr[b_frame],
                    take_model,
                    class_idx,
                    return_map=False,
                    layer_name="block5_conv3",
                    zeroing=zeroing,
                    image_weight=1,
                    heatmap_weight=0.25
                )

            # compute uncertainty 
            if uncertainty_method is not None:
                precision = get_uncertainty(take_model, in_img, runs=10, method=uncertainty_method)
                precision_best_frames.append(precision)
            
        # Output
        if save_video_path is None:
            return cams
        else:
            for j in range(return_cams):
                copied_arr_hires[best_frames[j]] = cams[j]
                #out_cams = copied_arr_hires.copy()

                # Add uncertainty overlay if desired
                if uncertainty_method is not None:
                    copied_arr_hires[best_frames[j]] = overlay_precision_gauge(
                        copied_arr_hires[best_frames[j]], 
                        precision_best_frames[j][0]
                    )

                    #out_all = copied_arr_hires.copy()
            #copied_arr_hires = np.repeat(copied_arr_hires, 3, axis=0)
            # io.vwrite(
            #     save_video_path + ".mpeg",
            #     copied_arr,
            #     outputdict={"-vcodec": "mpeg2video"}
            # )
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            writer = cv2.VideoWriter('output.avi', fourcc, 10.0, cam_dims)
            for x in copied_arr_hires:
                writer.write(x.astype("uint8"))
            writer.release()

            #return out_cams, out_all 

    def read_video(self, video_path):
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
        preds_arr = np.array(preds)
        frame_scores = preds_arr[:, predicted_class]
        best_frames = np.argsort(frame_scores)[-n_return:]
        return best_frames
