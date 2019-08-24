import tempfile # можно юзать также io.StringIo (более легкий модуль)
import tarfile
import unittest
from os.path import join
import os
import json
from neural_network.maskCNN import Mask
import helpers.net as net



class DetectionsTest(unittest.TestCase):
    dirName = "detections"
    cacheDirectory = True

    TEST_IMAGE_DIR = join(os.getcwd(), "data", "test_images")

    def setUp(self):
        # скачаем тестовую обстановку
        link = "https://vk.com/doc84996630_511877903?hash=b0be058a17a0081383&dl=4ae52327d30cae1c59"
        name = f"{self.dirName}.tar.gz"
        archivePath = join(self.TEST_IMAGE_DIR, name)

        net.downloadAndMove(link, join(self.TEST_IMAGE_DIR, name))  # на этом этапе мы не знамем навзание фала по ссылке
        tar = tarfile.open(archivePath, 'r')
        tar.extractall(self.TEST_IMAGE_DIR)
        os.remove(archivePath)

    def test(self):
        mask = Mask()
        with open(os.path.join(self.TEST_IMAGE_DIR, 'detections', 'detections.json')) as json_file:
            data = json.load(json_file)

        for i, filename in enumerate(os.listdir(os.path.join(self.TEST_IMAGE_DIR, self.dirName))):
            filepath = os.path.join(self.TEST_IMAGE_DIR, self.dirName, filename)
            arg = mask.pipeline(filepath, os.path.join(self.TEST_IMAGE_DIR, 'detectionsOutput', filename))
            print(arg)
            print(data[filename])
            print(filename)
            self.assertEqual(arg, data[filename])

    def tearDown(self):
        if not self.cacheDirectory:
            from shutil import rmtree
            rmtree(join(self.TEST_IMAGE_DIR, "detections"))


if __name__ == '__main__':
    unittest.main()

