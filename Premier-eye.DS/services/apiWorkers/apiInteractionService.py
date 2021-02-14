from services.apiWorkers.baseInteractionService import BaseInteractionService
from sys import platform
from config.apiRoutes import galleryRoutes
import os
from config.settings import config
from Models import Image
import json


class ApiInteractionService(BaseInteractionService):
    async def postLog(self, title, timestamp, cameraId):
        return self.post(galleryRoutes['log'], json={'title': title, 'timestamp': timestamp.timestamp(), 'cameraId': cameraId})

    async def postImageInfo(self, imagePath: str, imageInfo):
        jsonInfo = {"objects": imageInfo.json()}
        return self.post(galleryRoutes['postInfo'](os.path.basename(imagePath)), json=jsonInfo)

    async def uploadImage(self, imagePath: str):
        if platform == "linux" or platform == "linux2":
            filename = os.path.split(imagePath)[1]  # TODO Only for linux!!
        else:
            filename = imagePath

        files = [('file', (filename, open(imagePath, 'rb'), 'image/jpg'))]

        return self.post(galleryRoutes['upload'](os.path.basename(filename)), files=files)

