from flask import Blueprint

blueprint = Blueprint(
    'gallery_blueprint',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='static'
)


routes = {
    'getImage': '/gallery/<filename>',
    'getAllImages': '/gallery',
    'getJsonInfo': '/gallery/<filename>/info',
    'getInfoFromCamera': '/gallery/camera/<cameraId>',
    'getImageBetweenDatesFromCamera': '/gallery/cameraDelta<cameraId>',
    'getObjectsFromRectangleOnImage': '/gallery/<filename>/objects',
    'getObjectsFromRectangleOnImageVisualize': '/gallery/<filename>/objectsVisualize'
}