from flask import render_template, url_for, send_from_directory
from application.main import bp
import os
from rq import Queue
from redis import Redis
import config


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# redisConn = Redis(host='redis', port="6379")
# queue = Queue(connection=redisConn)


@bp.route('/startDetection', methods=['GET'])
def startDetection():
    import application.services.docker_handlers as dc
    job = queue.enqueue(dc.runDockerContainer("sapfir0/premier-eye"))


@bp.route("/api/getUpdateKey", methods=['GET'])
def getUpdateKey():
    return NotImplemented  # может вовзращать просто последнюю версию, чтобы сервисы обращзались сюда и обновлялись


@bp.route("/service/checkConnections", methods=['POST'])
def checkConnections():
    return NotImplemented


@bp.route('/favicon.ico')
def favicon():
    print(os.path.join(config.pyfrontDir, 'static', 'img'))
    return send_from_directory(os.path.join(config.pyfrontDir, 'static', 'img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
