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

api = Namespace('events')

@api.route(routes['log'])
class EventsLogger(Resource):

    cameraModel = getModel("Log", api, directory="DTO")
    @api.expect(cameraModel)
    def post(self):
        req = request.get_json()
        entity = Events(req['timestamp'], req['title'], req['cameraId'])
        db.session.add(entity)
    
        db.session.commit()

        return make_response({"success": "Log created"}, 200)

    # @api.response(200, cameraModel)
    def get(self):
        conn = db.engine.connect()
        selectStmt = select([Events])
        res = conn.execute(selectStmt).fetchall()
        stringRes = [dict(i) for i in res]
        return make_response({"data": stringRes}, 200)

