import os
from typing import Dict

from cameraFixedDest import cameras
from config import Config as cfg
from controllers.camera import namespace, routes
from database import db
from database.entities.cameras import DatabaseCameras
from database.models.Images import Images
from flask import (jsonify, make_response, redirect, request,
                   send_from_directory)
from flask_restplus import Namespace, Resource
from premier_eye_common.filename import getDateFromFilename, parseFilename
from services.directory import getOutputDir, recursiveSearch
from services.model import getModel
from werkzeug.datastructures import FileStorage

api = Namespace('camera')
cameraManager = DatabaseCameras()


@api.route(routes['getAllImagesFromCameras'])
class CameraImageList(Resource):
    def get(self, cameraId):
        """ Получить только изображения с камеры """
        cameraPath = os.path.join(cfg.UPLOAD_FOLDER, cameraId)

        if not os.path.exists(cameraPath):
            return make_response({"error": "Error while loading camera on filesystem"}, 400)

        lastImageDate = os.listdir(cameraPath)[-1]

        imgList = recursiveSearch(cameraPath)
        indexedImgList = [{'id': i, 'src': src} for i, src in enumerate(imgList)]
        return make_response({'images': indexedImgList}, 200)
        


@api.route(routes['getCamera'])
class Camera(Resource):

    cameraModel = getModel("Camera", api, directory="DTO", fullOutputName="CameraDto")
    @api.expect(cameraModel)
    def post(self, cameraId):
        """ Добавить новую камеру """
        cameraDTO = request.json
        cameraManager.postCamera(**cameraDTO)
        return make_response({'operation': 'success'}, 200)


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
        cameraList = cameraManager.listCameras(request.args)

        for cameraName in cameras: 
            index = next( (i for i,camera in enumerate(cameraList) if camera['name'] == str(cameraName)), None) # будет ошибка, если в бд нет такой камеры, которая есть в моих данных
            if index is not None:
                cameraList[index]['latlon'] = cameras[cameraName]['coordinates']
                cameraList[index]['view'] = cameras[cameraName]['view']
        
        return make_response({'items': cameraList}, 200)


