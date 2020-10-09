
from controllers.base import blueprint
from config import Config as cfg
from services.directory import getOutputDir
from controllers.base import routes
from database.models.Images import Images, session
import requests


@blueprint.route(routes['detectionList'], methods=['GET'])
def detectionList():
    return requests.get(cfg.detectionProgramUrl + routes['detectionList']).content


@blueprint.route(routes['deleteImage'], methods=['GET', 'POST'])
def deleteImage(filename):
    session.commit()
    session.flush()
# принимает src
# удалядет запись в бд и из фс

