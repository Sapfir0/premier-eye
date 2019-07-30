from flask import render_template, url_for, send_from_directory
from application.main import bp
import os
import config

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

from rq import Queue
from redis import Redis
redisConn = Redis(host='redis', port="6379")
queue = Queue(connection=redisConn)
job = queue.enqueue()
#while not job.result:
    # ждем

@bp.route('/startDetection')
def startDetection():
    import application.services.docker_handlers as dc
    dc.runDockerContainer("sapfir0/premier-eye")



@bp.route('/favicon.ico')
def favicon():
    print(os.path.join(config.pyfrontDir, 'static', 'img'))
    return send_from_directory(os.path.join(config.pyfrontDir, 'static', 'img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
