
namespace = '/gallery'

routes = {
    'image': '/image/<filename>',
    'getAllImages': '/images',
    'getImageInfo': '/<filename>/info',
    'getAllImagesFromCamera': '/camera/<string:cameraId>',
    'getImageBetweenDatesFromCamera': '/cameraDelta<string:cameraId>',
    'getObjectsFromRectangleOnImage': '/<filename>/objects',
    'getObjectsFromRectangleOnImageVisualize': '/<filename>/objectsVisualize'
}


