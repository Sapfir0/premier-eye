from flask import Flask
from redis import Redis
import rq
from config import Config


def runDetecting():
    import services.docker_handlers as dc
    dc.runDockerContainer("sapfir0/premier-eye")


def createApp(configClass=Config):
    app = Flask(__name__, template_folder="views")  # это экспортируем
    print(app.config)
    app.config.from_object(configClass)

    from app.errors import bp as errorsBP
    app.register_blueprint(errorsBP)

    from app.main import bp as mainBP
    app.register_blueprint(mainBP)
    return app

