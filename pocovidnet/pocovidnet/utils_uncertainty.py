'''
Compute uncertainty of classification results based on two methods:

    * epistemic: predict multiple times using dropout
    * aleatoric: augments data and then predicts multiple times

Contains two respective functions that each accept a model, an image and a runs
parameter. Both functions return a number in [0,1], where 0 indicates greatest
uncertainty.

NOTE: uncertainty always computed based on model from split 0 --
this is hardcoded as of now.

'''
import os
import numpy as np
import cv2


def overlay_precision_gauge(image, precision):
    """
    Returns the image overlaid with a tachometer-style
    gauge of precision in %.
    """
    #image = cv2.resize(image, (1000,1000))
    overlay = cv2.addWeighted(
        cv2.cvtColor(image.astype('uint8'), cv2.COLOR_RGB2BGR), 1,
        fetch_precision_overlay(precision), 1, 0
    )
    return overlay


def fetch_precision_overlay(precision):
    """
    Returns the overlay for the given precision value as cv2 image.
    """

    overlay_folder = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '../assets/precision_overlays'
    )

    img_path = os.path.join(
        overlay_folder, f'overlay_{str(int(precision*100)).zfill(3)}.png'
    )
    assert os.path.isfile(img_path), f'overlay does not exist at {img_path}'

    return cv2.imread(img_path)


def confidence_to_precision(x, lb=0.0, ub=0.5):
    x_clipped = np.clip(x, lb, ub)
    x_out = -(x_clipped - lb) / (ub - lb) + 1
    return x_out


def confidence_bar(img, value):
    x_len, y_len, _ = img.shape
    block_width = y_len // 10
    block_height = x_len // 3
    border = x_len // 50

    left = -border - block_width
    right = -border
    bottom = -border

    # make bar weight
    img[bottom - block_height:bottom, left:right] = [255, 255, 255]

    # compute colour and bar height
    normed_col_val = int(value * 255)
    normed_height_val = int(value * block_height)

    # color the coloured part
    img[bottom -
        normed_height_val:bottom, left:right] = [100, normed_col_val, 100]
    return img
