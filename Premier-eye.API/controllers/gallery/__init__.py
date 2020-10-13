
namespace = '/gallery'

routes = {
    'image': '/image/<filename>',
    'getCameras': '/cameraList',
    'getAllImages': '/images',
    'getImageInfo': '/image/<filename>/info',
    'getImageInfoByIndexOfImage': '/image/info',
    'getAllImagesFromCamera': '/camera/<string:cameraId>',
    'getImageBetweenDatesFromCamera': '/cameraDelta<string:cameraId>',
    'getObjectsFromRectangleOnImage': '/<filename>/objects',
    'getObjectsFromRectangleOnImageVisualize': '/<filename>/objectsVisualize'
}


