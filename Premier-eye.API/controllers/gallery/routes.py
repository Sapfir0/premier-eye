import os
from flask import jsonify, send_from_directory, request, make_response
from typing import List
from flask import redirect, request
from werkzeug.utils import secure_filename
from services.directory import recursiveSearch, getOutputDir
from controllers.gallery import routes, namespace
import database.dbAPI as db
from datetime import datetime
from flask_restplus import Namespace, Resource
import os
import json
from services.jsonWorking import addObjectToSession
from config import Config as cfg
from services.directory import getOutputDir
from database.models.Images import Images, session
from werkzeug.datastructures import FileStorage

api = Namespace('gallery')

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', help='Camera file',
                           type=FileStorage, required=True)
upload_parser.add_argument('')


@api.route(routes['image'])
class Image(Resource):
    @api.response(400, "Incorrect filename")
    @api.response(404, "Image not found")
    @api.response(200, "Return image")
    def get(self, filename):
        outputPath = os.path.join(cfg.UPLOAD_FOLDER, getOutputDir(filename))
        if os.path.exists(outputPath):
            return send_from_directory(os.path.split(outputPath)[0], filename)
        else:
            return make_response({"error": "Error while loading image"}, 404)

    @api.expect(upload_parser)
    def post(self, filename):
        def allowedFile(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in cfg.ALLOWED_EXTENSIONS

        if 'file' not in request.files and request.files['file'].filename == '':
            return make_response({"error": "No image"}, 400)

        file = request.files['file']
        if not file and not allowedFile(file.filename):
            return make_response({"error": "Incorrect file"}, 400)

        imageInfo = request.form
        if not imageInfo['objects'] or not imageInfo['numberOfCam'] or not imageInfo['fixationDatetime']:
            return make_response({"error": "Incorrect image info"})

        filename = secure_filename(file.filename)
        outputPath = os.path.join(cfg.UPLOAD_FOLDER, getOutputDir(filename))
        if not os.path.exists(os.path.split(outputPath)[0]):
            os.makedirs(os.path.split(outputPath)[0])
        file.save(outputPath)

        image = Images(outputPath, imageInfo['filename'], int(imageInfo['numberOfCam']), datetime.strptime(imageInfo['fixationDatetime'], '%Y-%m-%d %H:%M:%S'))
        session.add(image)  # TODO вынести работу с БД в другой поток, она долгая

        # fixedImageInfo = imageInfo['objects'].replace('car', '"car"').replace('person', '\'person\'')
        # print(fixedImageInfo)
        # dictObjects = eval(fixedImageInfo)
        # print(dictObjects)
        # addObjectToSession(dictObjects)

        session.commit()
        session.flush()

        return make_response({'success': 'Image created'}, 200)


@api.route(routes['getAllImages'])
class ImageList(Resource):
    @api.response(200, "Success")
    def get(self):
        return jsonify(recursiveSearch(cfg.UPLOAD_FOLDER))


@api.route(routes['getImageInfo'])
class ImageInformation(Resource):
    def get(self, filename):
        imageInfo = db.getImageByFilename(filename)

        if imageInfo is None:
            return "Image not found", 404

        if imageInfo['hasObjects']:
            objectInfo = db.getObjects(filename)
            imageInfo.update({"objects": objectInfo})

        return jsonify(dict(imageInfo))


@api.route(routes['getAllImagesFromCamera'])
class CameraImagesList(Resource):
    def get(self, cameraId):
        cameraPath = os.path.join(cfg.UPLOAD_FOLDER, cameraId)
        if not os.path.exists(cameraPath):
            return jsonify({"error": "Error while loading camera"}), 400
        imgList = recursiveSearch(cameraPath)
        return jsonify(imgList)


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


@api.route(routes['getObjectsFromRectangleOnImageVisualize'], methods=['POST'])
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

