from flask import jsonify, make_response, request
from controllers.objectInfo import routes
import database.dbAPI as db
from flask_restplus import Namespace, Resource, fields
from database.models.Cars import Cars
from database.models.Persons import Persons
from database.models.Objects_ import Objects_
from database.models.Images import Images, session
from database.models.Coordinates import Coordinates
from services.model import getModel
import os
from config import Config
from services.directory import recursiveSearch, getOutputDir
from services.model import getModel


api = Namespace('objectInfo')

@api.route(routes['getObjectInfoByIndexOfImage'])
class ObjectInformation(Resource):
    model = getModel("ObjectInfo", api)

    @api.response(200, "Success", model)
    def get(self):
        pass


