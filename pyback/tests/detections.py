import tempfile # можно юзать также io.StringIo (более легкий модуль)
import tarfile
from helpers.others import downloadAndMove
import unittest
from os.path import join
from settings import Settings as cfg
import os
import json
from neural_network.maskCNN import Mask


class DetectionsTest(unittest.TestCase):
    dirName = "detections"
    def setUp(self):
        # скачаем тестовую обстановку
        link = "https://vk.com/doc84996630_511676458?hash=e915563b619b68d654&dl=c0802c3ea67efa693e"
        name = f"{self.dirName}.tar.gz"
        downloadAndMove(link, join(cfg.TEST_IMAGE_DIR, name))  # на этом этапе мы не знамем навзание фала по ссылке
        archivePath = join(cfg.TEST_IMAGE_DIR, name)
        tar = tarfile.open(archivePath, 'r')
        tar.extractall(cfg.TEST_IMAGE_DIR)
        os.remove(archivePath)

    def test(self):
        mask = Mask()
        with open('detections.json') as json_file:
            data = json.load(json_file)
            print(data)
        for filename in os.listdir(cfg.TEST_IMAGE_DIR, self.dirName):
            _f, _f2, arg = mask.pipeline(filename)
            self.assertEqual()

    # def tearDown(self):
    #     from shutil import rmtree
    #     rmtree(join(cfg.TEST_IMAGE_DIR, "detections"))


if __name__ == '__main__':
    unittest.main()

