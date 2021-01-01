from config import Config as cfg
from importlib import import_module
from flask import Flask, url_for
from flask_cors import CORS
from config import Config
from database import db
from docs import api


def createApp(configClass=Config):
    staticFolder = 'static'
    configApp = Flask(__name__, static_folder=staticFolder)
    configApp.config.from_object(configClass)
    CORS(configApp, resources={r'/*': {'origins': '*'}})
    
    return configApp


app = createApp(cfg)
api.init_app(app)

if __name__ == '__main__':
    app.run(port=cfg.PORT, host=cfg.HOST)