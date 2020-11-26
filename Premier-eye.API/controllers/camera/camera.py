from flask import jsonify, send_from_directory, request, make_response
from flask import redirect, request
from typing import Dict
from controllers.camera import routes, namespace
from flask_restplus import Namespace, Resource
import os
from config import Config as cfg
from services.directory import getOutputDir
from database.models.Images import Images, session
from werkzeug.datastructures import FileStorage
from premier_eye_common.filename import parseFilename
from services.model import getModel
from services.directory import recursiveSearch


api = Namespace('camera')

@api.route(routes['getAllImagesFromCamera'])
class CameraImageList(Resource):
    model = getModel("CameraImageList", api)

    @api.response(200, "Success", model)
    def get(self, cameraId):
        cameraPath = os.path.join(cfg.UPLOAD_FOLDER, cameraId)
        if not os.path.exists(cameraPath):
            return make_response({"error": "Error while loading camera"}, 400)
        imgList = recursiveSearch(cameraPath)
        return make_response({'items': imgList}, 200)


@api.route(routes['getCameraList'])
class CamerasList(Resource):
    model = getModel("CameraList", api)

    @api.response(200, "Success", model)
    def get(self):
        cameraPath = os.path.join(cfg.UPLOAD_FOLDER)
        return make_response({'items': os.path.listdir(cameraPath)}, 200)



@api.route(routes['getCamera'])
class ObjectInformation(Resource):
    model = getModel("Camera", api)

    @api.response(200, "Success", model)
    def get(self, cameraId):
        pass
