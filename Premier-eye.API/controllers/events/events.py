from flask import jsonify, send_from_directory, request, make_response
from flask import redirect, request
from typing import Dict
from controllers.events import routes, namespace
from flask_restplus import Namespace, Resource
import os
from config import Config as cfg
from services.directory import getOutputDir
from database.models.Events import Events
from werkzeug.datastructures import FileStorage
from premier_eye_common.filename import parseFilename
from services.model import getModel
from database import db
import datetime
from sqlalchemy import select, insert
from database.entities.events import DatabaseEvents

api = Namespace('events')

@api.route(routes['log'])
class EventLogger(Resource):
    eventsManager = DatabaseEvents()

    cameraModel = getModel("Log", api, directory="DTO")
    @api.expect(cameraModel)
    def post(self):
        req = request.get_json()
        self.eventsManager.postEvent(timestamp=req['timestamp'], title=req['title'], cameraId=req['cameraId'])
        return make_response({"success": "Log created"}, 200)

    @api.response(200, "Success", cameraModel)
    def get(self):
        stringRes = self.eventsManager.listEvents()
        return make_response({"data": stringRes}, 200)


@api.route(routes['logs'])
class EventsLogger(Resource):
    eventsManager = DatabaseEvents()

    cameraModel = getModel("Logs", api, directory="DTO")
    @api.expect(cameraModel)
    def post(self):
        req = request.get_json()
        for title in req['titles']:
            self.eventsManager.postEvent(timestamp=req['timestamp'], title=title, cameraId=req['cameraId'])
        return make_response({"success": "Log created"}, 200)


