from flask import Flask, jsonify, request
import cv2
import os
from pocovidnet.evaluate_covid19 import Evaluator

UPLOAD_FOLDER = os.path.join(
    os.path.expanduser('~'), 'codevscovid', 'covid_detector',
    'covid19_pocus_ultrasound', 'data', 'pocus', 'cleaned_data_images'
)

model = Evaluator(ensemble=False)
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
        filename = str(request.args.get('fn', "1,1,1,1,1"))

    # fn = "test.jpg"
    img = cv2.imread(os.path.join(UPLOAD_FOLDER, filename))
    print(img.shape)
    out_preds = model(img)

    test_dict = {"image shape": img.shape, "prediction": str(out_preds)}
    return jsonify(test_dict)  # return json file


if __name__ == '__main__':

    app.run(debug=True)
