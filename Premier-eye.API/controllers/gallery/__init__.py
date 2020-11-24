
namespace = '/gallery'

routes = {
    'image': '/image/<filename>',
    'getCameras': '/cameraList',
    'getAllImages': '/images',
    'getImageInfo': '/image/<filename>/info',
    'getImageInfoByIndexOfImage': '/image/info',
    'getImageObjectInfoByIndexOfImage': '/image/objectInfo', # нужно только для правильной  типизации, т.к. я не понял как выделить objectInfo, если его никто не возвращает
    'getAllImagesFromCamera': '/camera/<string:cameraId>',
    'getImageBetweenDatesFromCamera': '/cameraDelta<string:cameraId>',
    'getObjectsFromRectangleOnImage': '/<filename>/objects',
    'getObjectsFromRectangleOnImageVisualize': '/<filename>/objectsVisualize'
}


