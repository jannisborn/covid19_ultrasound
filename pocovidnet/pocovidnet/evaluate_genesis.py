import numpy as np
import os
from pocovidnet import VIDEO_MODEL_FACTORY
from pocovidnet.videoto3d import Videoto3D
from tensorflow.keras import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling3D

NUM_FOLDS = 5


class GenesisEvaluator():

    def __init__(
        self,
        weights_dir="video_genesis_lr1e4",
        ensemble=True,
        split=None,
        model_id="genesis"
    ):
        """
        Constructor of COVID model evaluator class.

        Arguments:
            ensemble {str} -- Whether the model ensemble is used.
            num_classes: must be 3 or 4, how many classes the model was
            trained on
        """
        # self.root = os.path.join('/', *DIR_PATH.split('/')[:-1])
        self.split = split
        self.ensemble = ensemble

        if model_id not in VIDEO_MODEL_FACTORY.keys():
            raise ValueError(
                f'Wrong model {model_id}. Options:{VIDEO_MODEL_FACTORY.keys()}'
            )
        else:
            self.model_id = model_id

        if ensemble:
            # retores 5 weight paths
            self.weights_paths = [
                os.path.join(
                    weights_dir,
                    'fold_' + str(fold),
                    "best_weights",
                    "variables",
                    "variables"
                ) for fold in range(NUM_FOLDS)
            ]
        else:
            if split is None or split < 0 or split > 4:
                raise ValueError(f'Provide split between 0 and 4, not {split}')
            self.weights_paths = [
                os.path.join(
                    # self.root
                    weights_dir,
                    'fold_' + str(self.split), 
                    "best_weights",
                    "variables",
                    "variables"
                )
            ]

        self.class_mappings = ['covid', 'pneunomia', 'regular']
        # Get Genesis base model
        base_models = [
            VIDEO_MODEL_FACTORY[self.model_id](
                (1, 64, 64, 32), batch_normalization=True
            ) for _ in range(len(self.weights_paths))
        ]
        # Get model head
        self.models = []
        for mod in base_models:
            x = mod.get_layer('depth_7_relu').output
            x = GlobalAveragePooling3D()(x)
            x = Dense(1024, activation='relu')(x)
            output = Dense(len(self.class_mappings), activation='softmax')(x)
            head_model = Model(inputs=mod.input, outputs=output)
            self.models.append(head_model)

        # restore weights
        try:
            for model, path in zip(self.models, self.weights_paths):
                model.load_weights(path)
        except Exception:
            raise Exception('Error in model restoring.')

        print(f'Model restored. Class mappings are {self.class_mappings}')

    def __call__(self, video_path, width=64, depth=5, fr=5):
        # read in video
        vid3d = Videoto3D("", width, width, depth, fr)
        vid3d.max_vid = {"cov": 20, "pne": 20, "reg": 20}
        X_test, _, fn = vid3d.video3d(
            [video_path], ["cov"]
        )  # cov as dummy label
        print(X_test.shape)
        assert len(np.unique(fn)) == 1, "ERROR WRONG FILEs!"

        # prepare for genesis
        X_test = np.transpose(X_test, [0, 4, 2, 3, 1])
        X_test = np.repeat(X_test, [6, 7, 7, 6, 6], axis=-1)
        # res = self.models[0].predict(X_test[0])
        # RUN
        res = [model.predict(X_test) for model in self.models]
        return np.array(res)
