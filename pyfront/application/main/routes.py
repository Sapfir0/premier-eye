from flask import render_template, url_for
from application.main import bp


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

import rq
# import Redis

@bp.route('/startDetection')
def startDetection():
    import application.services.docker_handlers as dc
    dc.runDockerContainer("sapfir0/premier-eye")


