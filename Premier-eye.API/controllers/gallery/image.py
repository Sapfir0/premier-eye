from flask import jsonify, send_from_directory, request, make_response
from flask import redirect, request
from werkzeug.utils import secure_filename
from controllers.gallery import routes, namespace
from datetime import datetime
from flask_restplus import Namespace, Resource
import os
from config import Config as cfg
from services.directory import getOutputDir
from database.models.Images import Images, session
from werkzeug.datastructures import FileStorage
import sys
sys.path.append('..')
from Common.services.filename import parseFilename


def initImage(api):
    upload_parser = api.parser()
    upload_parser.add_argument('file', location='files', help='Image from camera', type=FileStorage, required=True)

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

            outputPath = os.path.join(cfg.UPLOAD_FOLDER, getOutputDir(filename))
            if not os.path.exists(os.path.split(outputPath)[0]):
                os.makedirs(os.path.split(outputPath)[0])
            file.save(outputPath)

            try:
                date, numberOfCam = parseFilename(filename, True, True)
            except:
                return make_response({"error": "Incorrect filename"}, 400)

            image = Images(outputPath, filename, int(numberOfCam), date)

            existingImage = session.query(Images).filter(Images.filename == filename).all()
            if existingImage:
                return make_response({"error": "Image with this filename exists"}, 400)

            session.add(image)  # TODO вынести работу с БД в другой поток, она долгая

            session.commit()
            session.flush()

            return make_response({'success': 'Image created'}, 200)
