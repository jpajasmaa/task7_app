from flask import Flask, request
from flask_restful import Api, Resource
import os
import sys
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer


from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
# Some utilites
import numpy as np

app = Flask(__name__)
api = Api(app)


subscription_key = "" 
endpoint = ""

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
print('Connected to Azure vision API, go to http://127.0.0.1:5000/')


@app.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')


@app.route('/classify', methods=['GET', 'POST'])
def classify():
    if request.method == 'POST':
        url = request.json
        print(url)

        # give url to the service
        tags_result_remote = computervision_client.tag_image(img)

        # Print results with confidence score
        print("Tags in the remote image: ")
        if (len(tags_result_remote.tags) == 0):
            print("No tags detected.")
        else:
            for tag in tags_result_remote.tags:
                
                print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))
        print()

        # 
        res = "put results to this string"

        return jsonify(result=res)


if __name__ == "__main__":
    #app.run()
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
