"""
Evaluation class that performs forward pass through trained models
"""
#%%
import os

import cv2
import numpy as np
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import (
    AveragePooling2D, Dense, Dropout, Flatten, Input
)
from tensorflow.keras.models import Model

from covid_detector.utils import CLASS_MAPPINGS


#%%
class Evaluator(object):

    def __init__(self, modality='pocus'):
        """
        Constructor of COVID model evaluator class.
        
        Arguments:
            modality {str} -- The data modality to be used. Chose from
                {'pocus', 'xray', 'ct'}, defaults to 'pocus'.
        """

        if modality not in ['pocus', 'xray', 'splitted']:
            raise ValueError(f'Unknown modality provided: {modality}')

        self.modality = modality
        self.num_classes = 3 if modality == 'pocus' else 2
        self.weights_path = os.path.join(
            '..', 'trained_models', modality + '.model'
        )
        self.class_mappings = CLASS_MAPPINGS[self.modality]

        # load the VGG16 network, ensuring the head FC layer sets are left off
        baseModel = VGG16(
            weights="imagenet",
            include_top=False,
            input_tensor=Input(shape=(224, 224, 3))
        )

        # construct the head of the model that will be placed on top of the
        # the base model
        headModel = baseModel.output
        headModel = AveragePooling2D(pool_size=(4, 4))(headModel)
        headModel = Flatten(name="flatten")(headModel)
        headModel = Dense(64, activation="relu")(headModel)
        headModel = Dropout(0.5)(headModel)
        headModel = Dense(self.num_classes, activation="softmax")(headModel)

        # place the head FC model on top of the base model
        self.model = Model(inputs=baseModel.input, outputs=headModel)

        # restore weights
        try:
            self.model.load_weights(self.weights_path)
        except Exception:
            raise Exception('Error in model restoring.')

        print(f'Model restored. Class mappings are {self.class_mappings}')

    def __call__(self, image):
        """Performs a forward pass through the restored model

        Arguments:
            image {np.array} -- Input image on which prediction is performed. 
                No size requirements, but the image will be reshaped to 224 x
                224 pixels (aspec ratio is *not* preserved, so quadratic images
                are preferred).

        Returns:
            logits {np.array} -- Shape (self.num_classes,). Class probabilities
                for 2 (or 3) classes.
        """

        image = self.preprocess(image)
        return np.squeeze(self.model.predict(image))

    def preprocess(self, image):
        """Apply image preprocessing pipeline

        Arguments:
            image {np.array} -- Arbitrary shape, quadratic preferred

        Returns:
            np.array -- Shape 224,224. Normalized to [0, 1].
        """

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (224, 224))
        image = np.expand_dims(np.array(image), 0) / 255.0
        return image
