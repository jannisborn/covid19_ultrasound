from flask import Flask, jsonify, request
import cv2
import os
from pocovidnet.evaluate_covid19 import Evaluator

model = Evaluator(ensemble=True)

app = Flask(__name__)

#set paths to upload folder
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['IMAGE_UPLOADS'] = os.path.join(APP_ROOT, 'static')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Receives a query to compute directions from source to directions (accesses
    GoogleMaps API). Can be called in GET or in POST mode.

    In any case, 'source' and 'destination' should be given in URL.
    """

    image = request.files['file']
    filename = image.filename
    file_path = os.path.join(app.config["IMAGE_UPLOADS"], filename)

    img = cv2.imread(file_path)
    if img is not None:
        out_preds = str(model(img))
    else:
        out_preds = "wrong image path"
    # return json file
    return jsonify(out_preds)


if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False, threaded=False, port=8000)
