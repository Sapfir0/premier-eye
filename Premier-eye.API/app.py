from config import Config as cfg
from importlib import import_module
from flask import Flask, url_for
from flask_cors import CORS
from config import Config

def registerBlueprints(app):
    modules = ['base', 'gallery']
    for moduleName in modules:
        module = import_module(f'controllers.{moduleName}.routes')
        app.register_blueprint(module.blueprint)


def createApp(configClass=Config):
    staticFolder = 'static'
    app = Flask(__name__, static_folder=staticFolder)
    app.config.from_object(configClass)
    registerBlueprints(app)
    CORS(app, resources={r'/*': {'origins': '*'}})
    return app


app = createApp(cfg)


if __name__ == '__main__':
    app.run(port=cfg.PORT, host=cfg.HOST)