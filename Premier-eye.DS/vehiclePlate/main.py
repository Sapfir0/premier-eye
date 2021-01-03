#!/bin/python
from flask import Flask, jsonify, request, make_response
from detector import read_number_plates
import os.path
from typing import Dict
import matplotlib.image as mpimg


UPLOAD_FOLDER = os.path.abspath(os.path.join(".", "images"))
if (not os.path.exists(UPLOAD_FOLDER)):
    os.mkdir(UPLOAD_FOLDER)

app = Flask(__name__)


@app.route('/status')
def status():
    return "alive"


# POST multipart
@app.route('/read')
def read():
    # можно еще передевать путем, но есть проблема, что контейнеры должны иметь общее volume
    arguments: Dict = request.files.to_dict()

    if ('file' not in arguments or request.files['file'].filename == ''):
        return make_response({"error": "No image"}, 400)
    
    file = request.files['file']
    if not file and not allowedFile(file.filename):
        return make_response({"error": "Incorrect file"}, 400)

    imgPath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(imgPath)
    img = mpimg.imread(imgPath)

    number_plates, region_names = read_number_plates(img)
    return jsonify({
        'success': True,
        'filename': file.filename,
        'number_plates': number_plates,
        'region_names': region_names,
    })

if __name__ == "__main__":
    print("Nomeroff-net active")
    app.run(port=5051, host='0.0.0.0')
