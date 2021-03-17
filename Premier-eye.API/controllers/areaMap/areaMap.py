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
from controllers.areaMap.cameraFixedDest import cameras
from services.geo import getLatLongDistance, getTrapeziumHeight

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
            print(currentCamera)
            CDx, CDy = rect.getCenterOfDown()
            print(CDx, CDy)
            latlongCoordinates.append(currentCamera['coordinates'])

        return jsonify(latlongCoordinates)
