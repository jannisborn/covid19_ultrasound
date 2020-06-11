import os
import sys
import random
import string
import secrets

# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Some utilites
import numpy as np
from util import base64_to_pil


# Declare a flask app
app = Flask(__name__)


# You can use pretrained model from Keras
# Check https://keras.io/applications/
from keras.applications.mobilenet_v2 import MobileNetV2
model = MobileNetV2(weights='imagenet')

print('Model loaded. Check http://127.0.0.1:5000/')


# Model saved with Keras model.save()
MODEL_PATH = 'models/your_model.h5'

# Load your own trained model
# model = load_model(MODEL_PATH)
# model._make_predict_function()          # Necessary
# print('Model loaded. Start serving...')


def model_predict(img, model):
    img = img.resize((224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    x = preprocess_input(x, mode='tf')

    preds = model.predict(x)
    return preds


@app.route('/predict', methods=['GET'])
def predict():
    # Main page
    return render_template('predict.html')

@app.route('/', methods=['GET'])
def index():
    return "Hello"


@app.route('/upload', methods=['GET'])
def upload():
    # Main page
    return render_template('upload.html')


@app.route('/predictbackend', methods=['POST'])
def predict_backend():
    if request.method == 'POST':
        # Get the image from post request
        img = base64_to_pil(request.json)

        # Save the image to ./uploads
        # img.save("./uploads/image.png")

        # Make prediction
        preds = model_predict(img, model)

        # Process your result for human
        pred_proba = "{:.3f}".format(np.amax(preds))    # Max probability
        pred_class = decode_predictions(preds, top=1)   # ImageNet Decode

        result = str(pred_class[0][0][1])               # Convert to string
        result = result.replace('_', ' ').capitalize()
        
        # Serialize the result, you can add additional fields
        return jsonify(result=result, probability=pred_proba)

    return None

@app.route('/uploadbackend/<label>', methods=['POST'])
def upload_backend(label):
    if request.method == 'POST':
        # Get the image from post request
        img = base64_to_pil(request.json)
        img.save("uploads/" + label + "/" + str(secrets.token_hex(32)) + ".png")
        return jsonify(result="Thank you!")
    return None

if __name__ == '__main__':
    #app.run(port=5002, threaded=False)

    # # Serve the app with gevent
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
