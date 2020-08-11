"""
Core Module for Grad CAM Algorithm
"""
from pathlib import Path

import cv2
import numpy as np
import tensorflow as tf


class GradCAM:
    """
    Perform Grad CAM algorithm for a given input
    Paper: [Grad-CAM: Visual Explanations from Deep Networks
            via Gradient-based Localization](https://arxiv.org/abs/1610.02391)
    """

    def explain(
        self,
        image,
        model,
        class_index,
        layer_name=None,
        colormap=cv2.COLORMAP_JET,
        zeroing=0.4,
        image_weight=1,
        heatmap_weight=0.25,
        return_map=True,
        size=(1000, 1000)
    ):
        """
        Compute GradCAM for a specific class index.
        Args:
            image (np.ndarray): Input image of shape: (x, x, 3)
            model (tf.keras.Model): tf.keras model to inspect
            class_index (int): Index of targeted class
            layer_name (str): Targeted layer for GradCAM. If no layer is
                provided, it is automatically infered from the model
                architecture.
            colormap (int): OpenCV Colormap to use for heatmap visualization
            zeroing -- Threshold between 0 and 1. Areas with a score below will
                be zeroed in the heatmap.
            image_weight -- float used to weight image when added to heatmap.
            heatmap_weight -- float used to weight heatmap when added to image.
            return_map --  Whether the heatmap is returned in addition to the
                image overlayed with the heatmap.
        Returns:
            numpy.ndarray: Grid of all the GradCAM
        """
        if size is None or not (isinstance(size, tuple) and len(size) == 2):
            print(
                f'size left undefined or not a 2-tuple - defaulting to (1000,1000)'
            )
            FINAL_RES = (1000, 1000)
        else:
            FINAL_RES = size

        if layer_name is None:
            layer_name = self.infer_grad_cam_target_layer(model)
        outputs, guided_grads = GradCAM.get_gradients_and_filters(
            model, [image], layer_name, class_index
        )

        cams = GradCAM.generate_ponderated_output(outputs, guided_grads)
        cam = cams[0].numpy()
        cam = cv2.resize(cam, (image.shape[1], image.shape[0]))

        cam = (cam - np.min(cam)) / (cam.max() - cam.min())

        heatmap = cv2.applyColorMap(
            cv2.cvtColor((cam * 255).astype("uint8"), cv2.COLOR_GRAY2BGR),
            colormap
        )
        heatmap[np.where(cam < zeroing)] = 0
        if np.max(image) <= 1:
            image = (image * 255).astype(int)
        overlay = cv2.cvtColor(
            cv2.addWeighted(
                cv2.cvtColor(image.astype('uint8'), cv2.COLOR_RGB2BGR),
                image_weight, heatmap, heatmap_weight, 0
            ), cv2.COLOR_BGR2RGB
        )
        overlay = cv2.resize(overlay, FINAL_RES)
        if return_map:
            return overlay, cam
        else:
            return overlay

    @staticmethod
    def infer_grad_cam_target_layer(model):
        """
        Search for the last convolutional layer to perform Grad CAM, as stated
        in the original paper.
        Args:
            model (tf.keras.Model): tf.keras model to inspect
        Returns:
            str: Name of the target layer
        """
        for layer in reversed(model.layers):
            # Select closest 4D layer to the end of the network.
            if len(layer.output_shape) == 4:
                return layer.name

        raise ValueError(
            "Model does not contain 4D layer. Grad CAM cannot be applied."
        )

    @staticmethod
    @tf.function
    def get_gradients_and_filters(model, images, layer_name, class_index):
        """
        Generate guided gradients and convolutional outputs with an inference.
        Args:
            model (tf.keras.Model): tf.keras model to inspect
            images (numpy.ndarray): 4D-Tensor with shape (batch_size, H, W, 3)
            layer_name (str): Targeted layer for GradCAM
            class_index (int): Index of targeted class
        Returns:
            Tuple[tf.Tensor, tf.Tensor]: Target layer outputs, Guided gradients
        """
        grad_model = tf.keras.models.Model(
            [model.inputs], [model.get_layer(layer_name).output, model.output]
        )

        with tf.GradientTape() as tape:
            inputs = tf.cast(images, tf.float32)
            conv_outputs, predictions = grad_model(inputs)
            loss = predictions[:, class_index]

        grads = tape.gradient(loss, conv_outputs)

        guided_grads = (
            tf.cast(conv_outputs > 0, "float32") *
            tf.cast(grads > 0, "float32") * grads
        )

        return conv_outputs, guided_grads

    @staticmethod
    def generate_ponderated_output(outputs, grads):
        """
        Apply Grad CAM algorithm scheme.
        Inputs are the convolutional outputs (shape WxHxN) and gradients
            (shape WxHxN).
        From there:
            - we compute the spatial average of the gradients
            - we build a ponderated sum of the convolutional outputs based on
                those averaged weights
        Args:
            output (tf.Tensor): Target layer outputs, with shape (batch_size,
                Hl, Wl, Nf), where Hl and Wl are the target layer output height
                and width, and Nf the number of filters.
            grads (tf.Tensor): Guided gradients with shape (bs, Hl, Wl, Nf)
        Returns:
            List[tf.Tensor]: List of ponderated output of shape (bs, Hl, Wl, 1)
        """

        maps = [
            GradCAM.ponderate_output(output, grad)
            for output, grad in zip(outputs, grads)
        ]

        return maps

    @staticmethod
    def ponderate_output(output, grad):
        """
        Perform the ponderation of filters output with respect to average of
            gradients values.
        Args:
            output (tf.Tensor): Target layer outputs, with shape (Hl, Wl, Nf),
                where Hl and Wl are the target layer output height and width,
                and Nf the number of filters.
            grads (tf.Tensor): Guided gradients with shape (Hl, Wl, Nf)
        Returns:
            tf.Tensor: Ponderated output of shape (Hl, Wl, 1)
        """
        weights = tf.reduce_mean(grad, axis=(0, 1))

        # Perform ponderated sum : w_i * output[:, :, i]
        cam = tf.reduce_sum(tf.multiply(weights, output), axis=-1)

        return cam

    def save(self, image, output_dir, output_name):
        """
            Save the output to a specific dir.
            Save a 3D Numpy array (H, W, 3) as an image.
            Args:
                image (numpy.ndarray): Image.
                output_dir (str): Output directory path
                output_name (str): Output name
            """
        Path.mkdir(Path(output_dir), parents=True, exist_ok=True)

        cv2.imwrite(
            str(Path(output_dir) / output_name),
            cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        )
