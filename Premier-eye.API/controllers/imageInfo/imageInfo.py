import os
from config import Config
from controllers.imageInfo import routes
from database import db
from database.entities.image import DatabaseImage
from database.entities.objectInfo import DatabaseObject
from database.models.Cars import Cars
from database.models.Coordinates import Coordinates
from database.models.Objects_ import Objects_
from database.models.Persons import Persons
from flask import jsonify, make_response, request
from flask_restplus import Namespace, Resource, fields
from services.directory import getOutputDir, recursiveSearch
from services.model import getModel

api = Namespace('imageInfo')

def getDatabaseModel(modelName, **args):
    models = {
        'car': Cars(**args),
        'person': Persons(**args)
    }
    return models[modelName]

@api.route(routes['getImageInfo'])
class ImageInformation(Resource):
    objectManager = DatabaseObject()
    imageManager = DatabaseImage()

    def get(self, filename):
        imageInfo = dict(self.imageManager.getImageByFilename(filename))

        if imageInfo is None:
            return make_response({"error": "Image not found"}, 400)

        objectInfo = self.objectManager.getObjectOnImage(imageInfo['id'])
        imageInfo.update({"objects": objectInfo})
        return jsonify(imageInfo)


    model = getModel("ImageInfo", api)
    @api.expect(model)
    def post(self, filename):
        currentImage = self.imageManager.getImageByFilename(filename)
        if currentImage == None:
            return make_response({"error": f"Image with {filename} filename not found"}, 400)
        imageId = currentImage['id']

        objects = request.json['objects']
        countOfObjectsIndbAPI = self.objectManager.getRowsCount() + 1  # т.к. мы только сейчас инсертим координаты

        for detected in objects:
            coordinates = Coordinates(detected['coordinates'])
            Object = Objects_(scores=detected['scores'], type=detected['type'],
                                imageId=imageId, coordinatesId=countOfObjectsIndbAPI)

            if detected['type'] == 'car': 
                car = Cars(carNumber=detected['vehiclePlate'], objectId=countOfObjectsIndbAPI)
                db.session.add(car)
            elif detected['type'] == 'person':
                person = Persons(objectId=countOfObjectsIndbAPI)
                db.session.add(person)
            else:
                make_response({"error": "Undefined object"}, 400)

            db.session.add(coordinates)
            db.session.add(Object)

            db.session.commit()
        db.session.flush()
        make_response({"success": "Info updated"}, 200)


imageInfoIndex = api.parser()
imageInfoIndex.add_argument('cameraId', location='args', type=str, required=True)
imageInfoIndex.add_argument('indexOfImage', location='args', type=str, required=True)

@api.route(routes['getImageInfoByIndexOfImage'])
class ImageInfoByIndexOfImage(Resource):
    objectManager = DatabaseObject()
    imageManager = DatabaseImage()

    @api.expect(imageInfoIndex)
    def get(self):
        query = request.args

        cameraPath = os.path.join(Config.UPLOAD_FOLDER, query['cameraId'])

        if not os.path.exists(cameraPath):
            return make_response({"error": "Error while loading camera"}, 400)
        imgList = recursiveSearch(cameraPath)
        filename = imgList[int(query['indexOfImage'])]

        imageInfo = self.imageManager.getImageByFilename(filename)
        objectInfo = self.objectManager.getObjectOnImage(imageInfo['id'])

        imageInfo.update({"objects": objectInfo})

        return make_response(dict(imageInfo), 200)
