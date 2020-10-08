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
    'getImage': f'{namespace}/<filename>',
    'getAllImages': f'{namespace}/images',
    'getImageInfo': f'{namespace}/<filename>/info',
    'getAllImagesFromCamera': f'{namespace}/camera/<cameraId>',
    'getImageBetweenDatesFromCamera': f'{namespace}/cameraDelta<cameraId>',
    'getObjectsFromRectangleOnImage': f'{namespace}/<filename>/objects',
    'getObjectsFromRectangleOnImageVisualize': f'{namespace}/<filename>/objectsVisualize'
}