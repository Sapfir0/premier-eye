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
from flask_socketio import SocketIO
from sockets.sockets import initSocket, socketio


def createApp(configClass=Config):
    staticFolder = 'static'
    configApp = Flask(__name__, static_folder=staticFolder)
    configApp.config.from_object(configClass)
    CORS(configApp, resources={r'/*': {'origins': '*'}})
    createLogger(configApp)
    api.init_app(configApp)
    return configApp


app = createApp(cfg)
initSocket(app)

if __name__ == '__main__':
    socketio.run(app, host=cfg.HOST, port=cfg.PORT)
