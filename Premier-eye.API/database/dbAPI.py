from sqlalchemy import select, insert
from sqlalchemy import and_
from database.models.Images import Images as Image
from database import db
from database.models.Objects_ import Objects_ as Object_
from database.models.Coordinates import Coordinates
from database.models.Camera import Camera
from datetime import datetime

def addNewCamera(cameraDto):
    conn = db.engine.connect()
    
    selectStmt = (insert(Camera).values(**cameraDto))
    res = conn.execute(selectStmt)
    return dict(res)

def getImageByFilename(filename):
    conn = db.engine.connect()

    selectStmt = select([Image]).where(Image.filename == filename)
    res = conn.execute(selectStmt).fetchone()  # можно сделать fetchall и если будет больше одного результата, вернуть фолс
    if res is None:
        return res
    return dict(res)


def getAllFilenames():
    conn = db.engine.connect()
    selectStmt = select([Image.filename])
    res = conn.execute(selectStmt).fetchall()
    stringRes = [i[0] for i in res]
    return stringRes


def getCamera(cameraId: int):
    conn = db.engine.connect()
    selectStmt = select([Camera.id])
    res = conn.execute(selectStmt).fetchall()
    stringRes = [i[0] for i in res]
    return stringRes


def getObjects(filename):
    conn = db.engine.connect()
    selectStmt = select([Object_]).where(and_(Object_.imageId == Image.id, Image.filename == filename))
    objectsInfo = conn.execute(selectStmt).fetchall()  # т.к. объектов может быть много
    if objectsInfo is None:
        raise ValueError(f"Objects not found on database")
    stringRes = [dict(i) for i in objectsInfo]
    return stringRes


def getImageBetweenDatesFromCamera(cameraId, startDate: datetime, endDate: datetime):
    conn = db.engine.connect()
    selectStmt = select([Image]).where(and_(Image.numberOfCam == cameraId,
                                            Image.fixationDatetime >= startDate,
                                            Image.fixationDatetime <= endDate))
    images = conn.execute(selectStmt).fetchall()
    stringRes = [list(i) for i in images]
    return stringRes


def getCoord(filename):
    conn = db.engine.connect()
    idImage = select([Image.id]).where(filename == Image.filename)
    coordinates = select([Coordinates.LDx, Coordinates.LDy,
                          Coordinates.RUx, Coordinates.RUy])\
        .where(and_(idImage == Object_.imageId,
               Coordinates.id == Object_.id))

    objectsInfo = conn.execute(coordinates).fetchall()
    stringRes = [list(i) for i in objectsInfo]
    return stringRes


