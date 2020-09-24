import argparse
import os

import cv2
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import tensorflow as tf

from pocovidnet.evaluate_covid19 import Evaluator
from pocovidnet.grad_cam import GradCAM

# Suppress logging
tf.get_logger().setLevel('ERROR')

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    '-d', '--data_dir', required=True, help='Path to input dataset'
)
ap.add_argument(
    '-m', '--model_dir', required=True, help='Path to model weights'
)
ap.add_argument(
    '-o', '--output_dir', required=True, help='Path to save heatmaps'
)
args = vars(ap.parse_args())

# Initialize hyperparameters
DATA_DIR = args['data_dir']
MODEL_DIR = args['model_dir']
OUTPUT_DIR = args['output_dir']

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

############ INSERT HERE CODE TO RESTORE THE MODEL ######
models = Evaluator(
    weights_dir=MODEL_DIR, ensemble=False, split=1, num_classes=3
)
model = models.models[-1]
print(model.summary())

############ INSERT HERE CODE TO RESTORE THE MODEL #######

gradcam = GradCAM()

for idx, filename in enumerate(os.listdir(DATA_DIR)):
    if filename.startswith("."):
        continue

    if idx % 10 == 0:
        print(f'Process file {idx}/{len(os.listdir(DATA_DIR))}')

    filepath = os.path.join(DATA_DIR, filename)
    img_loaded = cv2.imread(filepath)
    #### TODO: Apply any image preprocessing here if applicable (?) ###
    img = models.preprocess(img_loaded)[0]
    #### TODO: Apply any image preprocessing here if applicable (?) ###

    #### TODO: Infer class index (for which class the CAM should be computed)
    class_index = 0
    #### TODO: Infer class index (for which class the CAM should be computed)

    overlay = gradcam.explain(
        img,
        model,
        class_index,
        return_map=False,
        image_weight=1,
        layer_name='block5_conv3',  # Tries to infer last 4D layer in network.
        # If it fails consider setting manually
        zeroing=0.65,
        heatmap_weight=0.25
    )

    plt.imshow(overlay)
    plt.savefig(os.path.join(OUTPUT_DIR, filename))

print('Done, shuttting down!')
