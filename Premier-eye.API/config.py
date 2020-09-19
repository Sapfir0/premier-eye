import os
from pathlib import Path


class Config(object):
    HOST = '0.0.0.0'

    FLASK_RUN_HOST = os.environ.get('FLASK_RUN_HOST', "localhost")
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    PORT = int(os.environ.get('FLASK_RUN_PORT', 8050))
    APP_PATH = Path(__file__).parents[0]
    serverUrl = f"http://{FLASK_RUN_HOST}:{PORT}/"

    detectionProgramUrl = "http://localhost:8010"

    UPLOAD_FOLDER = os.path.join(APP_PATH, "static", "uploads")
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

