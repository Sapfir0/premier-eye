import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
     