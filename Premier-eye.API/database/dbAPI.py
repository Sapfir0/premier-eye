from sqlalchemy import select
from sqlalchemy import and_
from database.models.Images import Images as Image
from database.models.Images import engine
from database.models.Objects_ import Objects_ as Object_
from database.models.Coordinates import Coordinates
from datetime import datetime



def getImageByFilename(filename):
    conn = engine.connect()

    selectStmt = select([Image]).where(Image.filename == filename)
    res = conn.execute(selectStmt).fetchone()  # можно сделать fetchall и если будет больше одного результата, вернуть фолс
    if res is None:
        raise ValueError(f"Image {filename} not found on database")
    return dict(res)


def getAllFilenames():
    conn = engine.connect()
    selectStmt = select([Image.filename])
    res = conn.execute(selectStmt).fetchall()
    stringRes = [i[0] for i in res]
    return stringRes


def getObjects(filename):
    conn = engine.connect()
    selectStmt = select([Object_]).where(and_(Object_.imageId == Image.id, Image.filename == filename))
    objectsInfo = conn.execute(selectStmt).fetchall()  # т.к. объектов может быть много
    if objectsInfo is None:
        raise ValueError(f"Objects not found on database")
    stringRes = [dict(i) for i in objectsInfo]
    return stringRes


def getImageBetweenDatesFromCamera(cameraId, startDate: datetime, endDate: datetime):
    conn = engine.connect()
    selectStmt = select([Image]).where(and_(Image.numberOfCam == cameraId,
                                            Image.fixationDatetime >= startDate,
                                            Image.fixationDatetime <= endDate))
    images = conn.execute(selectStmt).fetchall()
    stringRes = [list(i) for i in images]
    return stringRes


def getCoord(filename):
    conn = engine.connect()
    idImage = select([Image.id]).where(filename == Image.filename)
    coordinates = select([Coordinates.LDx, Coordinates.LDy,
                          Coordinates.RUx, Coordinates.RUy])\
        .where(and_(idImage == Object_.imageId,
               Coordinates.id == Object_.id))

    objectsInfo = conn.execute(coordinates).fetchall()
    stringRes = [list(i) for i in objectsInfo]
    return stringRes





