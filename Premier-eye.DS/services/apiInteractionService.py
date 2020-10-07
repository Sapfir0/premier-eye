from services.baseInteractionService import BaseInteractionService
from sys import platform
import tempfile
from config.apiRoutes import galleryRoutes
import os
from config.settings import Settings


class ApiInteractionService(BaseInteractionService):
    # def __init__(self, config: Settings):
    #     super(config)


    def uploadImage(self, imagePath: str, image):

        if platform == "linux" or platform == "linux2":
            filename = os.path.split(imagePath)[1]  # TODO Only for linux!!
        else:
            filename = imagePath

        with tempfile.NamedTemporaryFile(delete=False) as temp:  # рр на винде приходится не юзать преимущества темфайла
            temp.write(image.json().encode('utf-8'))
            temp.flush()

            files = [
                ('file', (filename, open(imagePath, 'rb'), 'image/jpg')),
                ('json', (temp.name, open(temp.name, 'rb'), 'application/json'))]
            temp.close()
        # также я не удаляю файл, что нужно бы
        self.post(galleryRoutes['upload'],  files=files)

