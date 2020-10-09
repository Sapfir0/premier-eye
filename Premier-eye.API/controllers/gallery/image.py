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


def initImage(api):
    upload_parser = api.parser()
    upload_parser.add_argument('file', location='files', help='Camera file',
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

            session.commit()
            session.flush()

            return make_response({'success': 'Image created'}, 200)
