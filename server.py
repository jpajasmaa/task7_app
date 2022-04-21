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
import re
import base64
from PIL import Image
from io import BytesIO

##img = Image.open(image)
#trans = transforms.ToPILImage()
#trans1 = transforms.ToTensor()

def base64_to_pil(img_base64):
    image_data = re.sub('^data:image/.+;base64,', '', img_base64)
    pil_image = Image.open(BytesIO(base64.b64decode(image_data)))
    return pil_image

app = Flask(__name__)
api = Api(app)

def to_raw_image(img):
    img = re.sub('^data:image/.+;base64,', '', img)
    return bytearray(img)

IMG_LEN = 224
IMG_SHAPE = (IMG_LEN,IMG_LEN,3)

def preprocess(ds_row):
  
    # Image conversion int->float + resizing
    image = tf.image.convert_image_dtype(ds_row['image'], dtype=tf.float32)
    image = tf.image.resize(image, (IMG_LEN, IMG_LEN), method='nearest')
    
    # Onehot encoding labels

    return image#, label


subscription_key = "2c3c11f47df74807be37f2497ab81236"
endpoint = "https://tiesdeepvision.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
print('Connected to Azure vision API, go to http://127.0.0.1:5000/')


@app.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')


@app.route('/classify', methods=['GET', 'POST'])
def classify():
    if request.method == 'POST':
        import io
        # img = base64_to_pil(request.json)
        # img = to_raw_image(request.json)
        res = ""
        
        # how to drop local files not urls.
        img = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTN_BkkZzMNeEKNKHjy5BUVts7RV3kg55XoS2A5W3hICG7LiXO2P12n1rgB8tzD3Zk6RXA&usqp=CAU" 

        tags_result_remote = computervision_client.tag_image(img)

        # Print results with confidence score
        print("Tags in the remote image: ")
        if (len(tags_result_remote.tags) == 0):
            print("No tags detected.")
        else:
            for tag in tags_result_remote.tags:
                
                print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))
        print()


        return jsonify(result=res)


if __name__ == "__main__":
    #app.run()
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
