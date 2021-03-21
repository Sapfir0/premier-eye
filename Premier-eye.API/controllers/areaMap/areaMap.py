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
from services.geo import calibrateRect
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
                    objects.append(objOnImage[i])

        coordinates = []
        for obj in objects:
            coordinates.append({**coordinatesManager.getCoordinate(obj['coordinatesId'])})

        latlongCoordinates = []
        for i, coordinate in enumerate(coordinates):
            rect = Rectangle([coordinate['LUy'], coordinate['LUx'], coordinate['RDy'], coordinate['RDx']])
            currentObject = objects[i] # количество объектов == количество координат
            currentCamera = cameras[currentObject['cameraId']]
            CDx, CDy = rect.getCenterOfDown()
            print(CDx, CDy)
            ll = calibrateRect(*currentCamera['view'], int(CDx), int(CDy))
            latlongCoordinates.append({**currentObject, 'cameraId': currentObject['cameraId'], 'type': currentObject['type'], 'latlon': ll })

        return jsonify(latlongCoordinates)


# затычка для типов 
@api.route("/latlon")
class LatLon(Resource):
    model = getModel("LatLon", api)
    @api.response(200, "Success", model)
    def get(self):
        pass