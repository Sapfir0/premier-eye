from flask import jsonify
from controllers.gallery import routes
import database.dbAPI as db
from flask_restplus import Namespace, Resource
from services.jsonWorking import addObjectToSession


def initImageInfo(api):
    imageinfo_parser = api.parser()
    imageinfo_parser.add_argument('file', help='Image info', required=True)

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

        @api.expect(imageinfo_parser)
        def post(self, filename):
            addObjectToSession(dictObjects)

