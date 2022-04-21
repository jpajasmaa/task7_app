from flask import Flask, request
from flask_restful import Api, Resource
import os
import sys
import re
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer


from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from api_helper_functions import *

# Some utilites
import numpy as np

app = Flask(__name__)
api = Api(app)


subscription_key = "a213fbf607b041829b03643240c6218f"
endpoint = "https://tiesdeepvision.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
print('Connected to Azure vision API, go to http://127.0.0.1:5000/')


@app.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')


@app.route('/classify', methods=['GET', 'POST'])
def classify():
    if request.method == 'POST':
        url = request.json
        print(f"URL: {url}")

        app_id = re.search("id=([a-z.0-9]+)", url).group(1)
        print(app_id)

        icon_url, app_desc, review_comments = scrape_app_details(app_id)

        # give url to the service
        tags_result_remote = computervision_client.tag_image(icon_url)

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
