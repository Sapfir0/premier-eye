from flask_restplus import Api, Resource, fields
from controllers.image.image import api as imageApi
from controllers.computeImage.computeImage import api as computeApi
from controllers.camera.camera import api as cameraApi
from controllers.imageInfo.imageInfo import api as imageInfoApi
from controllers.objectInfo.objectInfo import api as objectInfoApi
from controllers.events.events import api as eventsApi
from controllers.areaMap.areaMap import api as areaMapApi

api = Api(
    title='Premier-eye API',
    version='0.1',
    description='Small API for object detecton',
)

api.add_namespace(imageApi)
api.add_namespace(computeApi)
api.add_namespace(cameraApi)
api.add_namespace(imageInfoApi)
api.add_namespace(objectInfoApi)
api.add_namespace(eventsApi)
api.add_namespace(areaMapApi)