from database.repo import Repo
from database.models.Coordinates import Coordinates

class DatabaseCoordinates(Repo):
    def listCoordinates(self, reqArgs):
        return self.all(Coordinates, reqArgs )
    
    def getCoordinate(self, id):
        return self.get(Coordinates, id)

    def postCoordinate(self, **entityFields):
        return self.post(Coordinates, **entityFields)
