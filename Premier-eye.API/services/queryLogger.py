from flask import Flask, url_for, g, request
import time
import datetime
import logging
import colorama
from colorama import init
from colorama import Fore, Back, Style


def createLogger(app):
    gunicorn_error_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.extend(gunicorn_error_logger.handlers)
    app.logger.setLevel(logging.DEBUG)
    log = logging.getLogger('werkzeug')
    log.disabled = True
    init()

    @app.before_request
    def start_timer():
        g.start = time.time()

    @app.after_request
    def log_request(response):
        now = time.time()
        duration = round(now - g.start, 2)
        dt = datetime.datetime.fromtimestamp(now)

        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        host = request.host.split(':', 1)[0]
        args = dict(request.args)
        log_params = [
            ('method', request.method, Fore.BLUE),
            ('path', request.path, Fore.BLUE),
            ('status', response.status_code,  Fore.YELLOW),
            ('duration', duration,  Fore.GREEN),
            # ('ip', ip,  Fore.RED),
            # ('host', host, Fore.RED),
            # ('params', args, Fore.BLUE)
        ]

        request_id = request.headers.get('X-Request-ID')
        if request_id:
            log_params.append(('request_id', request_id, 'yellow'))

        parts = []
        for name, value, color in log_params:
            part = color + "{}={}".format(name, value)
            parts.append(part)
        line = " ".join(parts)

        app.logger.info(line)

        return response
