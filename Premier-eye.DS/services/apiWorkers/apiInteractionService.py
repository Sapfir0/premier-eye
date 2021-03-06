from services.apiWorkers.baseInteractionService import BaseInteractionService
from sys import platform
from config.apiRoutes import galleryRoutes
import os
from config.settings import config
from Models import Image
import json
import asyncio


class ApiInteractionService(BaseInteractionService):

    async def postEvents(self, logStrings, timestamp, cameraId):
        if len(logStrings) == 0: 
            return
        date = timestamp.strftime('%Y-%m-%d %H:%M:%SZ') # default iso format
        return self.post(galleryRoutes['logs'], json={'titles': logStrings, 'timestamp': date, 'cameraId': cameraId})

    async def postLog(self, title, timestamp, cameraId):
        date = str(timestamp.utcnow())
        return self.post(galleryRoutes['log'], json={'title': title, 'timestamp': date, 'cameraId': cameraId})

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

