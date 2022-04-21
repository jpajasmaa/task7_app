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
        play_store_url = request.json

        res = "Results are: "
        print(f"URL: {play_store_url}")

        app_id = re.search("id=([a-z.0-9]+)", play_store_url).group(1)
        print(app_id)

        # example URL app
        # app_id = 'com.rovio.abclassic22'
        icon_url, app_desc, review_comments = scrape_app_details(app_id)

        icon_tags = get_icon_tags_azure(icon_url)
        print(f"Icon Tags: {icon_tags}")

        icon_desc = get_icon_description_azure(icon_url)
        print(f"Icon Description: {icon_desc}")

        description_entities = get_text_entities_gcp(app_desc)
        print(f"Key game features (description entities): {description_entities} ")

        positive, neutral, negative = get_reviews_sentiment_azure(review_comments)
        print(f"Review Sentiments: Positive({positive}), Neutral({neutral}), Negative({negative})")



        return jsonify(
            icon_t=str(icon_tags),
            icon_d=str(icon_desc),
            desc_e=str(description_entities),
            pos=str(positive),
            neu=str(neutral),
            neg=str(negative),
                       )


if __name__ == "__main__":
    #app.run()
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
