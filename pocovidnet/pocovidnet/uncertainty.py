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
from imutils import paths
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, confusion_matrix

from scipy import stats
import pickle
import pandas as pd
from scipy.stats import pearsonr
from sklearn.metrics import accuracy_score, balanced_accuracy_score, precision_score, recall_score

from pocovidnet.evaluate_covid19 import Evaluator

def get_uncertainty(model, image, runs=10, method='epistemic'):
    """
    Computes the precision of predictions of model given image. 
    method can either
        'epistemic' (dropout during inference) 
        'aleatoric' (test time augmentation)
    """
    
    #TODO: get model_id and num_classes from model by storing it in model.name

    if method == 'epistemic':
        dropout=True
        augment=False

    elif method == 'aleatoric':
        dropout=False
        augment=True 
    else:
        print(f"invalid method '{method}', needs to be 'epistemic' or 'aleatoric'")
        return 

    # initialize new model to ensure dropout is True TODO: make those hardcoded args dynamic
    model = Evaluator(ensemble=False, split=0, model_id='vgg_cam', num_classes=4, mc_dropout=dropout)
    
    # MAIN STEP: feed through model and compute logits {runs} times
    
    raw_logits = np.zeros((runs, len(model.class_mappings)))
    for idx in range(runs):      
        raw_logits[idx, :] = model(image, preprocess=False, augment=augment)

    # compute first two moments of predictions  
    logits_mean = np.mean(raw_logits, axis=0)
    logits_stds = np.std(raw_logits, axis=0)

    # get classification result
    pred_idx = np.argmax(logits_mean)
    classes = ["covid", "pneumonia", "regular", 'uninformative']
    pred_class = classes[pred_idx]

    precision = confidence_to_precision(logits_stds[pred_idx])

    return precision, pred_class

def overlay_precision_gauge(image, precision):
    """
    Returns the image overlaid with a tachometer-style
    gauge of precision in %.
    """
    #image = cv2.resize(image, (1000,1000))
    overlay = cv2.addWeighted(
        cv2.cvtColor(image.astype('uint8'), cv2.COLOR_RGB2BGR),
        1, fetch_precision_overlay(precision), 1, 0
    )
    return overlay

def fetch_precision_overlay(precision):
    """
    Returns the overlay for the given precision value as cv2 image.
    """

    overlay_folder = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            '../precision_overlays'
    )
    
    img_path = os.path.join(overlay_folder, f'overlay_{str(int(precision*100)).zfill(3)}.png')
    assert os.path.isfile(img_path), f'overlay does not exist at {img_path}'

    return cv2.imread(img_path)



def confidence_to_precision(x, lb=0.0, ub=0.5):
    x_clipped = np.clip(x, lb, ub)
    x_out = -(x_clipped-lb)/(ub-lb)+1 
    return x_out