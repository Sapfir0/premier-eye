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
    cacheDirectory = False

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
        with open(os.path.join(cfg.TEST_IMAGE_DIR, 'detections', 'detections.json')) as json_file:
            data = json.load(json_file)

        for filename in os.listdir(os.path.join(cfg.TEST_IMAGE_DIR, self.dirName)):
            _f,  arg = mask.pipeline(filename, None)
            self.assertEqual( arg, data[filename])

    def tearDown(self):
        if not self.cacheDirectory:
            from shutil import rmtree
            rmtree(join(cfg.TEST_IMAGE_DIR, "detections"))


if __name__ == '__main__':
    unittest.main()

