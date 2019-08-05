import tempfile # можно юзать также io.StringIo (более легкий модуль)
import tarfile
from helpers.others import downloadAndMove
import unittest
from os.path import join
from settings import Settings as cfg
import os
import  wget


class DetectionsTest(unittest.TestCase):
    def setUp(self):
        # скачаем тестовую обстановку
        link = "https://vk.com/doc84996630_511676458?hash=e915563b619b68d654&dl=c0802c3ea67efa693e"
        name = "detections.tar.gz"
        downloadAndMove(link, join(cfg.TEST_IMAGE_DIR, name))  # на этом этапе мы не знамем навзание фала по ссылке
        archivePath = join(cfg.TEST_IMAGE_DIR, name)
        tar = tarfile.open(archivePath, 'r')
        tar.extractall(cfg.TEST_IMAGE_DIR)
        os.remove(archivePath)

    def test(self):
        self.assertEqual(1+1, 2)

    def tearDown(self):
        import shutil
        os.removedirs(join(cfg.TEST_IMAGE_DIR, "detections"))


if __name__ == '__main__':
    unittest.main()

