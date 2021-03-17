from flask import jsonify, send_from_directory, request, make_response
from flask import redirect, request
from typing import Dict
from controllers.areaMap import routes, namespace
from flask_restplus import Namespace, Resource
import os
from config import Config as cfg
from premier_eye_common.filename import parseFilename
from services.model import getModel
from database import db
from services.decart import Rectangle
from database.entities.coordinates import DatabaseCoordinates
from database.entities.image import DatabaseImage
from database.entities.objectInfo import DatabaseObject
from services.geo import getLatLongDistance, getTrapeziumHeight, calibrateRect
from cameraFixedDest import cameras

api = Namespace('areaMap')

coordinatesManager = DatabaseCoordinates()
imageManager = DatabaseImage()
objectManager = DatabaseObject()

@api.route(routes['getAllObjectDest'])
class AreaMap(Resource):
    def get(self):
        reqArgs = request.form 
        images = imageManager.getNewestImageFromAllCamera()
        objects = []
        for image in images:
            objOnImage = objectManager.getObjectOnImage(image['id']) 
            for i, obj in enumerate(objOnImage):
                objOnImage[i] = {**obj, 'cameraId': image['numberOfCam'] }
            if (objOnImage != []):
                objects.append(*objOnImage)

        coordinates = []
        for obj in objects:
            coordinates.append({**coordinatesManager.getCoordinate(obj['coordinatesId'])})

        latlongCoordinates = []
        for i, coordinate in enumerate(coordinates):
            rect = Rectangle([coordinate['LDx'], coordinate['LDy'], coordinate['RUx'], coordinate['RUy']])
            currentObject = objects[i] # количество объектов == количество координат
            currentCamera = cameras[currentObject['cameraId']]
            imageWithLatLon = calibrateRect(*currentCamera['view'])
            CDx, CDy = rect.getCenterOfDown()
            print(CDx, CDy)
            ll = imageWithLatLon[int(CDx)][int(CDy)]
            latlongCoordinates.append({'cameraId': currentObject['cameraId'], 'type': currentObject['type'], 'lat': ll['lat'], 'lng': ll['lng'] })

        return jsonify(latlongCoordinates)


# затычка для типов 
@api.route("/latlon")
class LatLon(Resource):
    model = getModel("LatLon", api)
    @api.response(200, "Success", model)
    def get(self):
        pass