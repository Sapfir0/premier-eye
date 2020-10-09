import os
from flask import jsonify, send_from_directory, request, make_response
from typing import List
from flask import redirect, request
from werkzeug.utils import secure_filename
from controllers.base import blueprint
from services.directory import recursiveSearch, getOutputDir
from controllers.gallery import routes, namespace
import database.dbAPI as db
from datetime import datetime
from flask_restplus import Namespace, Resource
import os
import json
from services.jsonWorking import parseJson, addObjectToSession
from config import Config as cfg
from services.directory import getOutputDir
from database.models.Images import Images, session
from werkzeug.datastructures import FileStorage

api = Namespace('gallery')

upload_parser = api.parser()
upload_parser.add_argument('file', location='file',
                           type=FileStorage, required=True)


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

        print(request.files)

        if 'file' not in request.files and request.files['file'].filename == '':
            return make_response({"error": "No image"}, 400)
        if 'json' not in request.files:
            return make_response({"error": "No image info in json"}, 400)

        file = request.files['file']
        if not file and not allowedFile(file.filename):
            raise Exception

        filename = secure_filename(file.filename)
        outputPath = os.path.join(cfg.UPLOAD_FOLDER, getOutputDir(filename))
        if not os.path.exists(os.path.split(outputPath)[0]):
            os.makedirs(os.path.split(outputPath)[0])
        file.save(outputPath)

        rawJson: str = request.files['json'].read().decode("utf-8")
        # один из типов получение джсона(тут немного странный), я записываю джсон в файл на другой стороне, а тут ситываю
        deserializedJson: dict = json.loads(rawJson)

        image = Images(outputPath, *parseJson(deserializedJson))
        session.add(image)  # TODO вынести работу с БД в другой поток, она долгая
        addObjectToSession(deserializedJson)

        session.commit()
        session.flush()

        return redirect(f"/gallery/{filename}")


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


@blueprint.route(routes['getImageBetweenDatesFromCamera'], methods=['POST'])
def getImageBetweenDatesFromCamera(cameraId):
    from services.directory import datetimePattern
    req = request.form
    if not req['startDate'] or req['endDate']:
        return "Uncorrected query. Need to set start and end date.", 404

    start = datetime.strptime(req['startDate'], datetimePattern)
    end = datetime.strptime(req['endDate'], datetimePattern)
    obj = db.getImageBetweenDatesFromCamera(cameraId, start, end)
    return jsonify(obj)


@blueprint.route(routes['getObjectsFromRectangleOnImage'], methods=['POST'])
def getObjectsFromRectangleFromImage(filename):
    """
        подаем координаты прямоугоьника, возвращаются все события/объекты в дельтта окрестности от него
    """
    from services.decart import isCompletelyInside
    bigRect = list(request.form['rectangle'].split(", "))
    bigRect = list(map(int, bigRect))
    coord = db.getCoord(filename)
    a = [isCompletelyInside(bigRect, coordObj) for coordObj in coord]
    return jsonify(a)


@blueprint.route(routes['getObjectsFromRectangleOnImageVisualize'], methods=['POST'])
def getObjectsFromRectangleOnImageVisualize(filename):
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

