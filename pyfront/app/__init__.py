from flask import Flask
from celery import Celery
from pathlib import Path
import sys
import os

app = Flask(__name__, template_folder="views")

queue = Celery('tasks', backend='amqp', broker='ampq://')

pathToPyback = os.path.join(Path(__file__).parents[2], "pyback" )
sys.path.append(pathToPyback)

# @queue.task
# def runDetecting():
#     main = MainClass()



from app import routes