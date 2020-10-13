import unittest
from config import Config as cfg
import requests
import os


class UploadImage(unittest.TestCase):
    routeUrl = cfg.serverUrl + "gallery/image/" + "1_20190718144434.jpg"
    imageName = "1_20190718144434.jpg" # учитывай, что этого изображения быть в базе не должно
    testsPath = os.path.join(cfg.APP_PATH, "tests", "res")
    imagePath = os.path.join(testsPath, imageName)
    jsonName = "test.json"
    jsonPath = os.path.join(testsPath, jsonName)

    def addImage(self, files: list):
        files.append(('file', (self.imageName, open(self.imagePath, 'rb'), 'image/jpg')))
        return files

    def test_uploadImageWithInfoUniqueConstrainAreFailure(self):
        pass

    def test_TimeTestInCorrectSituation(self):
        pass

    def test_NoImageHere(self):
        files = []
        r = requests.post(self.routeUrl, files=files)
        self.assertEqual(400, r.status_code)


    def test_IncorrectJsonImageFixationDatetime(self):
        pass

    def test_IncorrectJsonImageNumberOfCamera(self):
        pass

    def test_IncorrectImageFilename(self):
        pass

    def test_ImageFilenameFromTheFutureMustBeDenied(self):
        pass

    def test_IncorrectImageExtension(self):
        pass

    def test_JsonNotInUtf8(self):
        pass

    def test_IncorrectPostBodySpecifier(self):
        pass

if __name__ == '__main__':
    unittest.main()
