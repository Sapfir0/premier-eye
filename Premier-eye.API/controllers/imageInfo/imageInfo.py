from flask import jsonify, make_response, request
from controllers.imageInfo import routes
import database.dbAPI as db
from flask_restplus import Namespace, Resource, fields
from database.models.Cars import Cars
from database.models.Persons import Persons
from database.models.Objects_ import Objects_
from database.models.Images import Images, session
from database.models.Coordinates import Coordinates
from services.model import getModel
import os
from config import Config
from services.directory import recursiveSearch, getOutputDir
from services.model import getModel



api = Namespace('imageInfo')

@api.route(routes['getImageInfo'])
class ImageInformation(Resource):
    def get(self, filename):
        imageInfo = db.getImageByFilename(filename)

        if imageInfo is None:
            return make_response({"error": "Image not found"}, 400)

        objectInfo = db.getObjects(filename)
        imageInfo.update({"objects": objectInfo})
        return jsonify(dict(imageInfo))


    model = getModel("ImageInfo", api)
    @api.expect(model)
    def post(self, filename):
        objects = request.json['objects']
        currentImage = session.query(Images).filter(Images.filename == filename).all()
        if len(currentImage) != 1:
            return make_response({"error": f"Image with {filename} filename not found"}, 400)
        imageId = currentImage[0].id
        # +1 т.к. у нас возвращается текущее колво строк, а мы будем инсертить еще одну
        countOfObjectsInDB = session.query(Objects_).count() + 1  # objectId TODO
        for detected in objects:
            coordinates = Coordinates(detected['coordinates'])
            Object = Objects_(scores=detected['scores'], type=detected['type'],
                                imageId=imageId, coordinatesId=countOfObjectsInDB)

            if detected['type'] == 'car':  # TODO кал
                car = Cars(carNumber=detected['licenseNumber'], objectId=countOfObjectsInDB)
                session.add(car)
            elif detected['type'] == 'person':
                person = Persons(objectId=countOfObjectsInDB)
                session.add(person)
            else:
                make_response({"error": "Undefined object"}, 400)

            session.add(coordinates)
            session.add(Object)

            session.commit()
            session.flush()

imageInfoIndex = api.parser()
imageInfoIndex.add_argument('cameraId', location='args', type=str, required=True)
imageInfoIndex.add_argument('indexOfImage', location='args', type=str, required=True)

@api.route(routes['getImageInfoByIndexOfImage'])
class ImageInfoByIndexOfImage(Resource):
    @api.expect(imageInfoIndex)
    def get(self):
        query = request.args

        cameraPath = os.path.join(Config.UPLOAD_FOLDER, query['cameraId'])
        if not os.path.exists(cameraPath):
            return jsonify({"error": "Error while loading camera"}), 400
        imgList = recursiveSearch(cameraPath)
        filename = imgList[int(query['indexOfImage'])]

        objectInfo = db.getObjects(filename)
        imageInfo = db.getImageByFilename(filename)
        imageInfo.update({"objects": objectInfo})
        print(objectInfo)

        return jsonify(dict(imageInfo))
