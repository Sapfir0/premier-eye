
namespace = '/gallery'

routes = {
    'image': '/image/<filename>',
    'getAllImages': '/images',
    'getImageInfo': '/<filename>/info',
    'getAllImagesFromCamera': '/camera/<int:cameraId>',
    'getImageBetweenDatesFromCamera': '/cameraDelta<int:cameraId>',
    'getObjectsFromRectangleOnImage': '/<filename>/objects',
    'getObjectsFromRectangleOnImageVisualize': '/<filename>/objectsVisualize'
}


