import os
from dotenv import load_dotenv

pyfrontDir = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.splitext(pyfrontDir)[0]
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
