from database.repo import Repo
from database.models.Objects_ import Objects_ as Objects
from database.models.Images import Images

class DatabaseObject(Repo):
    def listObjects(self):
        return self.all(Objects)
    
    def getObjectById(self, id):
        objects = self.get(Objects, id)
        return objects

    def getObjectOnImage(self, imageId):
        return self.getWhere(Objects, (Objects.imageId == imageId), multiple=True)


    def getRowsCount(self):
        return self.rowCount(Objects)

    def postObject(self, **entityFields):
        return self.post(Objects, **entityFields)
