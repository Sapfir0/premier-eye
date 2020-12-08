from config import Config as cfg
from importlib import import_module
from flask import Flask, url_for
from flask_cors import CORS
from config import Config
from docs import api
# from database import init_database

def createApp(configClass=Config):
    staticFolder = 'static'
    configApp = Flask(__name__, static_folder=staticFolder)
    configApp.config.from_object(configClass)
    CORS(configApp, resources={r'/*': {'origins': '*'}})
    # init_database()
    return configApp


app = createApp(cfg)
api.init_app(app)

if __name__ == '__main__':
    app.run(port=cfg.PORT, host=cfg.HOST)