from config import Config as cfg
from importlib import import_module
from flask import Flask, url_for, g, request
from flask_cors import CORS
from config import Config
from database import db, Database
from docs import api
import time
import datetime
from services.queryLogger import createLogger

def createApp(configClass=Config):
    staticFolder = 'static'
    configApp = Flask(__name__, static_folder=staticFolder)
    configApp.config.from_object(configClass)
    CORS(configApp, resources={r'/*': {'origins': '*'}})
    
    return configApp


app = createApp(cfg)
api.init_app(app)

createLogger(app)

if __name__ == '__main__':
    app.run(port=cfg.FLASK_RUN_HOST, host=cfg.HOST, threaded=True)