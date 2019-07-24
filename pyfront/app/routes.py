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
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)

@app.route('/index')
def playVideo():
    return "ss"


# app.add_url_rule('img/favicon.ico',
#                  redirect_to=url_for('static', filename='favicon.ico'))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico', mimetype='image/vnd.microsoft.icon')