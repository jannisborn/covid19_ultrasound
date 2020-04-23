from flask import Flask, jsonify, request
import cv2
import os
from pocovidnet.evaluate_covid19 import Evaluator

model = Evaluator(ensemble=True)

app = Flask(__name__)

#set paths to upload folder
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['IMAGE_UPLOADS'] = os.path.join(
    APP_ROOT, '..', '..', 'data', 'tmp_images'
)


def allowed_file(filename):
    return '.' in filename and \
           filename.split('.')[-1].lower() in ["jpg", "png", "jpeg"]


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


if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False, threaded=False, port=8000)
