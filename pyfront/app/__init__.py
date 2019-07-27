from flask import Flask
from celery import Celery
from pathlib import Path
import sys
import os

app = Flask(__name__, template_folder="views")

queue = Celery('tasks', backend='amqp', broker='ampq://')

@queue.task
def runDetecting():
    import services.docker_handlers as dc
    dc.runDockerContainer("sapfir0/premier-eye")


from app import routes