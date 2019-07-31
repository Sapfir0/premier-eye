from flask import Flask
from config import Config
from rq import Queue
from redis import Redis

def createApp(configClass=Config):
    app = Flask(__name__, template_folder="views")  # это экспортируем
    app.config.from_object(configClass)

    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.taskQueue = Queue('premier-eye', connection=app.redis)

    from application.errors import bp as errorsBP
    app.register_blueprint(errorsBP)

    from application.main import bp as mainBP
    app.register_blueprint(mainBP)

    return app

