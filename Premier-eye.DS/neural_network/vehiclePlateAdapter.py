import requests as _
from services.apiWorkers.apiInteractionService import ApiInteractionService
from config.settings import Settings
import services.timeChecker as timeChecker

@timeChecker.checkElapsedTime(7, 3, 2, "Car plate detecting")
def detectPlate(fullImagePath, api: ApiInteractionService):
    files = [('file', ('myimg', open(fullImagePath, 'rb'), 'image/jpg'))]
    return api.post('/read', files=files, host=Settings.nomeroffNetLink)
    