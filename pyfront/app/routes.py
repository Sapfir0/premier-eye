from flask import render_template, send_from_directory, url_for
from app import app
from pathlib import Path
import sys
import os
pathToPyback = os.path.join(Path(__file__).parents[2], "pyback" )
sys.path.append(pathToPyback)
#import mainImage


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/index')
def playVideo():
    return "ss"



@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico', mimetype='image/vnd.microsoft.icon')