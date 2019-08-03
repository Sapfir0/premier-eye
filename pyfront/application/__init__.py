from flask import Flask
from config import Config
from rq import Queue
from redis import Redis
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def createApp(configClass=Config):
    app = Flask(__name__, template_folder="views")  # это экспортируем
    app.config.from_object(configClass)

    db.init_app(app)
    migrate.init_app(app, db)

    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.taskQueue = Queue('premier-eye', connection=app.redis)

    from application.errors import bp as errorsBP
    app.register_blueprint(errorsBP)

    from application.main import bp as mainBP
    app.register_blueprint(mainBP)

    return app

