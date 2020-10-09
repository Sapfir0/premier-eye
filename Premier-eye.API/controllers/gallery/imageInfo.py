from flask import jsonify, make_response, request
from controllers.gallery import routes
import database.dbAPI as db
from flask_restplus import Namespace, Resource, fields
from database.models.Cars import Cars
from database.models.Persons import Persons
from database.models.Objects_ import Objects_
from database.models.Images import Images, session
from database.models.Coordinates import Coordinates


def initImageInfo(api: Namespace):
    model = api.model('ObjectInfo', {
        'id': fields.Integer,
        'type': fields.String,
        'scores': fields.Float,
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

        @api.expect(model)
        def post(self, filename):
            objects = request.form
            countOfImagesInDB = session.query(Images).count() + 1  # imageId
            # +1 т.к. у нас возвращается текущее колво строк, а мы будем инсертить еще одну
            countOfObjectsInDB = session.query(Objects_).count() + 1  # objectId TODO
            for detected in objects:
                coordinates = Coordinates(detected['coordinates'])
                Object = Objects_(scores=detected['scores'], typesOfObject=detected['type'],
                                  imageId=countOfImagesInDB, coordinatesId=countOfObjectsInDB)

                if detected['type'] == 'car':  # TODO кал
                    car = Cars(carNumber=detected['licenseNumber'], objectId=countOfObjectsInDB)
                    session.add(car)
                elif detected['type'] == 'person':
                    person = Persons(objectId=countOfObjectsInDB)
                    session.add(person)
                else:
                    make_response({"error": "Undefined object"}, 400)

                session.add(coordinates)
                session.add(Object)

                session.commit()
                session.flush()

