"""
Evaluation class that performs forward pass through trained models
"""
import os

import cv2
import numpy as np

from pocovidnet import MODEL_FACTORY

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
NUM_FOLDS = 5


class Evaluator(object):

    def __init__(self, ensemble=True, split=None, model_id=None):
        """
        Constructor of COVID model evaluator class.
        
        Arguments:
            ensemble {str} -- Whether the model ensemble is used.
        """
        self.root = os.path.join('/', *DIR_PATH.split('/')[:-1])
        self.split = split
        self.ensemble = ensemble
        if model_id is None:
            self.model_id = 'vgg_base'
        elif model_id not in MODEL_FACTORY.keys():
            raise ValueError(
                f'Wrong model {model_id}. Options are:{MODEL_FACTORY.keys()}'
            )
        else:
            self.model_id = model_id

        if ensemble:
            # retores 5 weight paths
            self.weights_paths = [
                os.path.join(
                    self.root, 'trained_models', 'fold_' + str(fold),
                    "variables", "variables"
                ) for fold in range(NUM_FOLDS)
            ]
        else:
            if split is None or split < 0 or split > 4:
                raise ValueError(f'Provide split between 0 and 4, not {split}')
            fold = split
            self.weights_paths = [
                os.path.join(
                    self.root, 'trained_models', 'fold_' + str(fold),
                    "variables", "variables"
                )
            ]

        self.class_mappings = ['covid', 'pneunomia', 'regular']
        self.models = [
            MODEL_FACTORY[self.model_id]()
            for _ in range(len(self.weights_paths))
        ]

        # restore weights
        try:
            for model, path in zip(self.models, self.weights_paths):
                model.load_weights(path)
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
            logits {list} -- Length 3 num_classes). Class probabilities.
        """

        image = self.preprocess(image)
        predictions = np.squeeze(
            np.stack([model.predict(image) for model in self.models]), axis=1
        )
        return list(np.mean(predictions, axis=0, keepdims=False))

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
