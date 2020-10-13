from flask import jsonify, send_from_directory, request, make_response
from flask import redirect, request
from services.directory import recursiveSearch, getOutputDir
from controllers.gallery import routes, namespace
import database.dbAPI as db
from datetime import datetime
from flask_restplus import Namespace, Resource
import os
from config import Config as cfg
from services.directory import getOutputDir
from controllers.gallery.imageInfo import initImageInfo
from controllers.gallery.image import initImage
from services.model import getModel

api = Namespace('gallery')
initImageInfo(api)
initImage(api)


@api.route(routes['getAllImages'])
class ImageList(Resource):
    model = getModel("ImageList", api)

    @api.response(200, "Success", model)
    def get(self):
        return make_response(recursiveSearch(cfg.UPLOAD_FOLDER), 200)

@api.route(routes['getAllImagesFromCamera'])
class CameraImagesList(Resource):
    def get(self, cameraId):
        cameraPath = os.path.join(cfg.UPLOAD_FOLDER, cameraId)
        if not os.path.exists(cameraPath):
            return jsonify({"error": "Error while loading camera"}), 400
        imgList = recursiveSearch(cameraPath)
        return jsonify(imgList)

@api.route(routes['getCameras'])
class CameraList(Resource):
    model = getModel("CameraList", api)

    @api.response(200, "Success", model)
    def get(self):
        cameras = os.listdir(cfg.UPLOAD_FOLDER)
        return make_response({'items': cameras}, 200)


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


@api.route(routes['getImageBetweenDatesFromCamera'])
class ImageByDateIntervalFromCamera(Resource):
    def get(self, cameraId):
        from services.directory import datetimePattern
        req = request.form
        if not req['startDate'] or req['endDate']:
            return "Uncorrected query. Need to set start and end date.", 404

        start = datetime.strptime(req['startDate'], datetimePattern)
        end = datetime.strptime(req['endDate'], datetimePattern)
        obj = db.getImageBetweenDatesFromCamera(cameraId, start, end)
        return jsonify(obj)


@api.route(routes['getObjectsFromRectangleOnImage'])
class ObjectsInRectangle(Resource):
    def get(self, filename):
        """
            подаем координаты прямоугоьника, возвращаются все события/объекты в дельтта окрестности от него
        """
        from services.decart import isCompletelyInside
        bigRect = list(request.form['rectangle'].split(", "))
        bigRect = list(map(int, bigRect))
        coord = db.getCoord(filename)
        a = [isCompletelyInside(bigRect, coordObj) for coordObj in coord]
        return jsonify(a)


@api.route(routes['getObjectsFromRectangleOnImageVisualize'])
class VisualizeObjectsFromRectangle(Resource):
    def get(self, filename):
        """
            подаем координаты прямоугольника, вовращается размеченное изображение
        """
        from services.decart import createGraphic
        path = getOutputDir(filename)

        bigRect = list(request.form['rectangle'].split(", "))
        bigRect = list(map(int, bigRect))
        coord = db.getCoord(filename)
        path = createGraphic(path, bigRect, coord)
        return send_from_directory(*path)

