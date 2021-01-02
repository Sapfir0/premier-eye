from flask import jsonify, send_from_directory, request, make_response
from flask import redirect, request
from typing import Dict
from controllers.camera import routes, namespace
from flask_restplus import Namespace, Resource
import os
from config import Config as cfg
from services.directory import getOutputDir
from database.models.Images import Images
from werkzeug.datastructures import FileStorage
from premier_eye_common.filename import parseFilename, getDateFromFilename
from services.model import getModel
from services.directory import recursiveSearch
from database.dbAPI import getCamera, addNewCamera
from database import db

api = Namespace('camera')

@api.route(routes['getAllImagesFromCameras'])
class CameraImageList(Resource):
    def get(self):
        pass
        

@api.route(routes['getCamera'])
class Camera(Resource):

    cameraModel = getModel("Camera", api, directory="DTO")
    @api.expect(cameraModel)
    def post(self):
        """ Добавить новую камеру """
        cameraDTO = request.json
        addNewCamera(cameraDTO)
        return make_response({'operation': 'success'})


    model = getModel("Camera", api)
    @api.response(200, "Success", model)
    def get(self, cameraId):
        """ Получить информацию о камере """
        cameraPath = os.path.join(cfg.UPLOAD_FOLDER, cameraId)

        if not os.path.exists(cameraPath):
            return make_response({"error": "Error while loading camera on filesystem"}, 400)

        lastImageDate = os.listdir(cameraPath)[-1]

        imgList = recursiveSearch(cameraPath)
        indexedImgList = [{'id': i, 'src': src} for i, src in enumerate(imgList)]
        return make_response({'images': indexedImgList, 'onlineDate': lastImageDate, 'id': cameraId}, 200)



@api.route(routes['getCameraList'])
class CamerasList(Resource):
    model = getModel("CameraList", api)

    @api.response(200, "Success", model)
    def get(self):
        """ Получить список камер """
        cameraPath = os.path.join(cfg.UPLOAD_FOLDER)
        cameraList = [{'id': camera} for camera in os.listdir(cameraPath)]

        return make_response({'items': cameraList}, 200)


