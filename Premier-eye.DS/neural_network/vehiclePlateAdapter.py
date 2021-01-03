import requests as _
from services.apiWorkers.apiInteractionService import ApiInteractionService
from config.settings import Settings

def detectPlate(fullImagePath, api: ApiInteractionService):
    files = [('file', ('myimg', open(fullImagePath, 'rb'), 'image/jpg'))]
    return api.post('/read', files=files, host=Settings.nomeroffNetLink)
    