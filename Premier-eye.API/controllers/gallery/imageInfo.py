from flask import jsonify, make_response
from controllers.gallery import routes
import database.dbAPI as db
from flask_restplus import Namespace, Resource, fields
from services.jsonWorking import addObjectToSession


def initImageInfo(api):
    model = api.model('ImageInfo', {

    })

    @api.route(routes['getImageInfo'])
    class ImageInformation(Resource):
        def get(self, filename):
            imageInfo = db.getImageByFilename(filename)

            if imageInfo is None:
                return make_response({"error": "Image not found"}, 400)

            if imageInfo['hasObjects']:
                objectInfo = db.getObjects(filename)
                imageInfo.update({"objects": objectInfo})

            return jsonify(dict(imageInfo))

        @api.marshal_with(model)
        def post(self, filename):
            addObjectToSession(dictObjects)

