from flask import Flask, jsonify, request
import cv2
import os
from pocovidnet.evaluate_covid19 import Evaluator
from evaluate_video import VideoEvaluator

import string 
import random

model = Evaluator(ensemble=True)

videoModel = VideoEvaluator()

app = Flask(__name__)

#set paths to upload folder
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['IMAGE_UPLOADS'] = os.path.join(
    APP_ROOT, '..', '..', 'data', 'tmp_images'
)


def allowed_file(filename):
    return '.' in filename and \
           filename.split('.')[-1].lower() in ["jpg", "png", "jpeg"]

def allowed_file_video(filename):
    return '.' in filename and \
           filename.split('.')[-1].lower() in ["mp4", "aac", "mov"]


@app.route('/predict', methods=['GET'])
def predict():
    """
    Receives a query to compute directions from source to directions (accesses
    GoogleMaps API). Can be called in GET or in POST mode.

    In any case, 'source' and 'destination' should be given in URL.
    """

    # OPTION 1: pass file
    # image = request.files['file']
    # filename = image.filename
    # OPTION 2: pass only the filename as argument
    filename = str(request.args.get('filename'))
    if filename is None or filename == "None":
        return jsonify("Need to pass argument filename to request! (empty)")
    # A filename arguemnt was passed
    if allowed_file(filename):
        # The filename is valid (jpg, jpeg or png)
        file_path = os.path.join(app.config["IMAGE_UPLOADS"], filename)
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
            return jsonify("Need to pass argument filename to request! (empty)")
        file = request.files['file']
        file_dir = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 24)) 
        if (allowed_file_video(file.filename) or allowed_file(file.filename)):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + file_dir, file.filename))
            return jsonify(app.config['UPLOAD_FOLDER'] + "/" + file_dir + file.filename)
        return jsonify("filename not allowed: " + file.filename)

@app.route("/video_predict", methods=['POST'])
def video_predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify("Need to pass argument filename to request! (empty)")
        file = request.files['file']
        file_dir = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 24)) 
        if (allowed_file_video(file.filename)):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + file_dir, file.filename))
            filepath = app.config['UPLOAD_FOLDER'] + "/" + file_dir + "/" +file.filename
            vidpath = app.config['UPLOAD_FOLDER'] + "/" + file_dir + "/" + "heatmap.mp4"
            preds = str(videoModel(filepath))
            videoModel.cam_important_frames(vidpath)
            return jsonify(videoModel(filepath) + vidpath)
        return jsonify("filename not allowed: " + file.filename)

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False, threaded=False, port=8000)
