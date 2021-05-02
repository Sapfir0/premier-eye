from flask import jsonify, send_from_directory, request, make_response
from flask import redirect, request
from typing import Dict
from controllers.image import routes, namespace
from flask_restplus import Namespace, Resource
import os
from config import Config as cfg
from services.directory import getOutputDir, recursiveSearch
from database.models.Images import Images
from werkzeug.datastructures import FileStorage
from premier_eye_common.filename import parseFilename
from services.model import getModel
from database import db
from database.entities.images import DatabaseImage


api = Namespace('gallery')

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', help='Image from camera', type=FileStorage, required=True)

imageManager = DatabaseImage()


@api.route(routes['getAllImages'])
class ImageList(Resource):
    model = getModel("ImageList", api)

    @api.response(200, "Success", model)
    def get(self):
        return make_response({'items': recursiveSearch(cfg.UPLOAD_FOLDER)}, 200)


@api.route(routes['image'])
class Image(Resource):  
    @api.response(400, "Incorrect filename")
    @api.response(404, "Image not found")
    @api.response(200, "Return image")
    def get(self, filename):
        try:
            outputPath = os.path.join(cfg.UPLOAD_FOLDER, getOutputDir(filename))
            if os.path.exists(outputPath):
                return send_from_directory(os.path.split(outputPath)[0], filename)
            else:
                return make_response({"error": "Error while loading image"}, 404)
        except:
            return make_response({"error": "Incorrect filename"}, 400)

    @api.expect(upload_parser)
    def post(self, filename):
        def allowedFile(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in cfg.ALLOWED_EXTENSIONS

        arguments: Dict = request.files.to_dict()

        if 'file' not in arguments or request.files['file'].filename == '':
            return make_response({"error": "No image"}, 400)

        file = request.files['file']
        if not file and not allowedFile(file.filename):
            return make_response({"error": "Incorrect file"}, 400)

        outputPath = os.path.join(cfg.UPLOAD_FOLDER, getOutputDir(filename))
        if not os.path.exists(os.path.split(outputPath)[0]):
            os.makedirs(os.path.split(outputPath)[0])
        file.save(outputPath)

        try:
            date, numberOfCam = parseFilename(filename, True, True)
        except:
            return make_response({"error": "Incorrect filename"}, 400)

        image = Images(outputPath, filename, int(numberOfCam), date)

        existingImage = imageManager.getImageByFilename(filename)
        if existingImage:
            return make_response({"error": "Image with this filename exists"}, 400)

        db.session.add(image)  # TODO вынести работу с БД в другой поток, она долгая

        db.session.commit()
        db.session.flush()

        return make_response({'success': 'Image created'}, 200)




@api.route(routes['imageById'])
class ObjectInformation(Resource):
    model = getModel("Image", api)

    @api.response(200, "Success", model)
    def get(self, imageById):
        pass
