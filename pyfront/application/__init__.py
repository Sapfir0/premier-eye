from flask import Flask
from config import Config


def createApp(configClass=Config):
    app = Flask(__name__, template_folder="views")  # это экспортируем
    app.config.from_object(configClass)

    from application.errors import bp as errorsBP
    app.register_blueprint(errorsBP)

    from application.main import bp as mainBP
    app.register_blueprint(mainBP)

    return app

