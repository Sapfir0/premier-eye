from database.repo import Repo
from database.models.Images import Images

class DatabaseImage(Repo):
    def listImages(self):
        return self.all(Images)
    
    def getImageById(self, id):
        return self.get(Images, id)

    def getImageByFilename(self, filename):
        return self.getWhere(Images, (Images.filename == filename))

    def postImage(self, **entityFields):
        return self.post(Images, **entityFields)
