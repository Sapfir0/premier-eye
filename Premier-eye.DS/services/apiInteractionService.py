from services.baseInteractionService import BaseInteractionService
from sys import platform
from config.apiRoutes import galleryRoutes
import os
from config.settings import Settings
from Models import Image
import json


class ApiInteractionService(BaseInteractionService):
    def postImageInfo(self, imageInfo):
        pass

    def uploadImage(self, imagePath: str):
        if platform == "linux" or platform == "linux2":
            filename = os.path.split(imagePath)[1]  # TODO Only for linux!!
        else:
            filename = imagePath

        files = [('file', (filename, open(imagePath, 'rb'), 'image/jpg'))]

        self.post(galleryRoutes['upload'](os.path.basename(filename)), files=files)

