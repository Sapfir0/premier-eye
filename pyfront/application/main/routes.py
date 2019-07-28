from flask import render_template, url_for
from application.main import bp

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')
