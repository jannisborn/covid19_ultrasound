from flask import Flask, jsonify, request
import cv2
import os
from pocovidnet.evaluate_covid19 import Evaluator

UPLOAD_FOLDER = os.path.join(
    '..', '..', 'data', 'pocus', 'cleaned_data_images'
)

model = Evaluator(ensemble=True)
app = Flask(__name__)


@app.route('/predict/', methods=['GET', 'POST'])
def query_directions():
    """
    Receives a query to compute directions from source to directions (accesses
    GoogleMaps API). Can be called in GET or in POST mode.

    In any case, 'source' and 'destination' should be given in URL.
    """

    if request.method == 'GET':
        # Parse arguments from query
        filename = str(request.args.get('fn', "None"))

    # read image
    img = cv2.imread(os.path.join(UPLOAD_FOLDER, filename))
    # run model
    if img is not None:
        out_preds = str(model(img))
    else:
        out_preds = "wrong image path"
    # return json file
    return jsonify(out_preds)


if __name__ == '__main__':

    app.run(debug=True)
