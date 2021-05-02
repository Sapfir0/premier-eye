from database.repo import Repo
from database.models.Cameras import Cameras

class DatabaseCameras(Repo):
    def listCameras(self, reqArgs):
        return self.all(Cameras, reqArgs)
    
    def getCamera(self, id):
        return self.get(Cameras, id)

    def postCamera(self, **entityFields):
        return self.post(Cameras, **entityFields)
