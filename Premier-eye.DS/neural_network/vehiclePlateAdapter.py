import requests as _
from services.apiWorkers.apiInteractionService import ApiInteractionService
from config.settings import Settings

def detectPlate(fullImagePath):
    return ApiInteractionService.get('/read', data={'url': fullImagePath}, host=Settings.nomeroffNetLink)
    