import os
from flask import jsonify, send_from_directory, request
from controllers.base import blueprint
from services.directory import recursiveSearch, getOutputDir
from config import Config as cfg
from controllers.gallery import routes
import database.dbAPI as db
from datetime import datetime


@blueprint.route(routes['getImage'])
def getImage(filename):
    try:
        outputPath = os.path.join(cfg.UPLOAD_FOLDER, getOutputDir(filename))
    except ValueError as err:
        return str(err), 404

    if os.path.exists(os.path.split(outputPath)[0]):
        return send_from_directory(os.path.split(outputPath)[0], filename)
    else:
        return jsonify({"error": "Error while loading image"}), 404


@blueprint.route(routes['getAllImages'], methods=['GET'])
def getAllImages():
    return jsonify(recursiveSearch(cfg.UPLOAD_FOLDER))

# функции, работающие с фс


@blueprint.route(routes['getJsonInfo'])
def getJsonInfo(filename):
    imageInfo = db.getImageByFilename(filename)

    if imageInfo is None:
        return "Image not found", 404

    if imageInfo['hasObjects']:
        objectInfo = db.getObjects(filename)
        imageInfo.update({"objects": objectInfo})

    return jsonify(dict(imageInfo))


@blueprint.route(routes['getInfoFromCamera'], methods=['GET'])
def getInfoFromCamera(cameraId):
    cameraPath = os.path.join(cfg.UPLOAD_FOLDER, cameraId)
    if not os.path.exists(cameraPath):
        return jsonify({"error": "Error while loading camera"}), 404
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

