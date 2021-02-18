from database.repo import Repo
from database.models.Events import Events

class DatabaseEvents(Repo):
    def listEvents(self):
        return self.all(Events)
    
    def getEvent(self, id):
        return self.get(Events)

    def postEvent(self, **entityFields):
        return self.post(Events, **entityFields)
