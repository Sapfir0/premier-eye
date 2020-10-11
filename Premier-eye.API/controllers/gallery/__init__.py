
namespace = '/gallery'

routes = {
    'image': '/image/<filename>',
    'getAllImages': '/images',
    'getImageInfo': '/image/<filename>/info',
    'getImageInfoByIndexOfImage': '/image/info',
    'getAllImagesFromCamera': '/camera/<string:cameraId>',
    'getImageBetweenDatesFromCamera': '/cameraDelta<string:cameraId>',
    'getObjectsFromRectangleOnImage': '/<filename>/objects',
    'getObjectsFromRectangleOnImageVisualize': '/<filename>/objectsVisualize'
}


