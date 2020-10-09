from flask import Blueprint

blueprint = Blueprint(
    'gallery_blueprint',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='static'
)

namespace = '/gallery'

routes = {
    'image': '/image/<filename>',
    'getAllImages': '/images',
    'getImageInfo': '/<filename>/info',
    'getAllImagesFromCamera': '/camera/<cameraId>',
    'getImageBetweenDatesFromCamera': '/cameraDelta<cameraId>',
    'getObjectsFromRectangleOnImage': '/<filename>/objects',
    'getObjectsFromRectangleOnImageVisualize': '/<filename>/objectsVisualize'
}


