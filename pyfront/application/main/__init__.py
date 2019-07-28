from flask import Blueprint

bp = Blueprint('main', __name__)

from application.main import routes