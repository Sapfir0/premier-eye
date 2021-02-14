from database.repo import Repo
from database.models.Images import Images
from datetime import datetime
from sqlalchemy import and_

class DatabaseImage(Repo):
    def listImages(self):
        return self.all(Images)
    
    def getImageById(self, id):
        return self.get(Images, id)

    def getImageByFilename(self, filename):
        return self.getWhere(Images, (Images.filename == filename))

    def postImage(self, **entityFields):
        return self.post(Images, **entityFields)

    def getImagesBetweenDatesFromCamera(self, cameraId, startDate: datetime, endDate: datetime):
        condition = and_(Images.numberOfCam == cameraId,
                                                Images.fixationDatetime >= startDate,
                                                Images.fixationDatetime <= endDate)
        images = self.getWhere(Images, condition, True)
        return images

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

