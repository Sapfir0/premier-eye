#!/bin/python
from flask import Flask, jsonify, request
from waitress import serve
from wtforms import Form, validators, StringField
from detector import read_number_plates

app = Flask(__name__)


@app.route('/status')
def status():
    return "alive"


@app.route('/read')
def read():
    form = request.args
    print(form)
    url = form['url']

    res = read_number_plates(url)
    if not res:
        return jsonify({
            'success': False,
            'errors': "Image path not correct, image not found"
        })
    else:
        number_plates, region_names = res
        return jsonify({
            'success': True,
            'url': url,
            'number_plates': number_plates,
            'region_names': region_names,
        })




def create_app():
    return serve(app)
