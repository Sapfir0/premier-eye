from flask import jsonify, send_from_directory, request, make_response
from flask import redirect, request
from typing import Dict
from controllers.computeImage import routes, namespace
from flask_restplus import Namespace, Resource
import os
from config import Config as cfg
from services.directory import getOutputDir
from database.models.Images import Images
from werkzeug.datastructures import FileStorage
from premier_eye_common.filename import parseFilename
from services.model import getModel
from database import db


api = Namespace('compute')

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

