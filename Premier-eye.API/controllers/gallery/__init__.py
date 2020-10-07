from flask import Blueprint

blueprint = Blueprint(
    'gallery_blueprint',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='static'
)

routes = {
    'getImage': '/<filename>',
    'getAllImages': '/gallery',
    'getJsonInfo': '/<filename>/info',
    'getInfoFromCamera': '/camera/<cameraId>',
    'getImageBetweenDatesFromCamera': '/cameraDelta<cameraId>',
    'getObjectsFromRectangleOnImage': '/<filename>/objects',
    'getObjectsFromRectangleOnImageVisualize': '/<filename>/objectsVisualize'
}