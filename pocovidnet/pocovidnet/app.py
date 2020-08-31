from flask import Flask, jsonify, request
import cv2
import os
from pocovidnet.evaluate_covid19 import Evaluator
from evaluate_video import VideoEvaluator
import string
import random

import string
import random
import numpy as np

videoModel = VideoEvaluator(
    weights_dir="../trained_models_cam",
    ensemble=True,
    model_id="vgg_cam",
    num_classes=4
)

app = Flask(__name__)

# set paths to upload folder
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(
    APP_ROOT, '..', '..', 'data', 'tmp_images'
)


def allowed_file(filename):
    return '.' in filename and \
           filename.split('.')[-1].lower() in ["jpg", "png", "jpeg"]


def allowed_file_video(filename):
    return '.' in filename and \
           filename.split('.')[-1].lower() in ["mp4", "mpg", "mov", "mpeg"]


def allowed_file_video(filename):
    return '.' in filename and \
           filename.split('.')[-1].lower() in ["mp4", "mpg", "mov", "mpeg", "avi", "gif"]


@app.route('/predict', methods=['GET'])
def predict():
    """
    Receives a query to compute directions from source to directions (accesses
    GoogleMaps API). Can be called in GET or in POST mode.
    In any case, 'source' and 'destination' should be given in URL.
    """
    filename = str(request.args.get('filename'))
    if filename is None or filename == "None":
        return jsonify("Need to pass argument filename to request! (empty)")
    # A filename arguemnt was passed
    if allowed_file(filename):
        # The filename is valid (jpg, jpeg or png)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        # read file
        img = cv2.imread(file_path)
        # check whether the file path was correct
        if img is not None:
            out_preds = str(model(img))
        else:
            out_preds = "image cannot be loaded from: " + file_path
        # return json of outputs
        return jsonify(out_preds)
    return jsonify("filename not allowed: " + filename)


@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify(
                "Need to pass argument filename to request! (empty)"
            )
        file = request.files['file']
        file_dir = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=24)
        )
        if (allowed_file_video(file.filename) or allowed_file(file.filename)):
            file.save(
                os.path.join(
                    app.config['UPLOAD_FOLDER'] + "/" + file_dir, file.filename
                )
            )
            return jsonify(
                app.config['UPLOAD_FOLDER'] + "/" + file_dir + file.filename
            )
        return jsonify("filename not allowed: " + file.filename)


@app.route("/video_predict", methods=['POST'])
def video_predict():
    """
    Receives query to screen a video: Predicts class and frame-wise confidence
    scores, and overlays the video with CAMs and certainty-gauge
    Arguments:
        The input video must be in the UPLOAD_FOLDER specified above!
        POST request must specify a file name, e.g. curl -F "image=@test.mp4"
    Returns:
        Predictions and file path to output video
    Debugging:
    - change file_dir (see comment bellow)
    - put a test video in a folder data/tmp_images/1234 (here named test.mp4)
    - run curl -F "image=@test.mp4" -X POST "http://0.0.0.0:8000/video_predict"
        (from the 1234 directory)
    """
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify(
                "Need to pass argument filename to request! (empty)"
            )
        file = request.files['image']
        file_dir = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=24)
        )
        # file_dir = "1234"  # for debugging:
        if (allowed_file_video(file.filename)) or allowed_file(file.filename):
            file.save(
                os.path.join(
                    app.config['UPLOAD_FOLDER'] + "/" + file_dir, file.filename
                )
            )
            filepath = app.config['UPLOAD_FOLDER'
                                  ] + "/" + file_dir + "/" + file.filename
            vidpath = app.config['UPLOAD_FOLDER'
                                 ] + "/" + file_dir + "/" + "heatmap"
            # get the predictions per frame
            vid_preds = videoModel(filepath)
            # take average
            preds = str(np.mean(vid_preds, axis=0))
            saved_path = videoModel.cam_important_frames(
                save_video_path=vidpath, uncertainty_method="epistemic"
            )
            return jsonify(preds + "\n" + saved_path)
        return jsonify("filename not allowed: " + file.filename)


if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False, threaded=False, port=8000)
