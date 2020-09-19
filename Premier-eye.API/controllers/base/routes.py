from flask import redirect, request
from werkzeug.utils import secure_filename
from controllers.base import blueprint

import os
import json

from services.jsonWorking import parseJson, addObjectToSession
from config import Config as cfg
from services.directory import getOutputDir
from controllers.base import routes

from database.models.Images import Images, session
import requests


@blueprint.route(routes['hi'], methods=['GET'])
def hi():
    return "Server is up!"


@blueprint.route(routes['detectionList'], methods=['GET'])
def detectionList():
    return requests.get(cfg.detectionProgramUrl + routes['detectionList']).content


@blueprint.route(routes['deleteImage'], methods=['GET', 'POST'])
def deleteImage(filename):
    session.commit()
    session.flush()
# принимает src
# удалядет запись в бд и из фс



@blueprint.route(routes['uploadFile'], methods=['POST'])
def uploadFile():
    def allowedFile(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in cfg.ALLOWED_EXTENSIONS

    print(request.form)
    print(request.files)
    print(request.args)

    if 'file' not in request.files and request.files['file'].filename == '':
        raise Exception("No image")
    if 'json' not in request.files:
        raise Exception("No image info in json")

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
