from flask import Blueprint

blueprint = Blueprint(
    'base_blueprint',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='static'
)

routes = {
    'uploadFile': '/upload',
    'hi': '/',
    'detectionList': '/detectionList',
    'deleteImage': '/deleteImage/<filename>'
}
