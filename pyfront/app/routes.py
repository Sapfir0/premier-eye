from flask import render_template, send_from_directory, url_for
from app import app
from pathlib import Path
import sys
import os


@app.route('/')
def index():
    return render_template('index.html', link="style.css")

@app.route('/settings')
def settings():
    return render_template('settings.html', title="Settings")



@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico', mimetype='image/vnd.microsoft.icon')
