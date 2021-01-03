import requests as _
from services.apiWorkers.apiInteractionService import ApiInteractionService
from config.settings import Settings

def detectPlate(fullImagePath):
    files = [('file', (filename, open(imagePath, 'rb'), 'image/jpg'))]
    return ApiInteractionService.post('/read', files=files, host=Settings.nomeroffNetLink)
    