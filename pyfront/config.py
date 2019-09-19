import os
from dotenv import load_dotenv

pyfrontDir = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.splitext(pyfrontDir)[0]
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    FLASK_RUN_HOST = os.environ.get('FLASK_RUN_HOST')
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    DATABASE_URL = os.environ.get("DATABASE_URL") or 'sqlite:///' + os.path.join(pyfrontDir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
