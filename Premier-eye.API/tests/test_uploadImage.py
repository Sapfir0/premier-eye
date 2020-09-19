import unittest
from config import Config as cfg
import requests
import os


class UploadImage(unittest.TestCase):
    routeUrl = cfg.serverUrl + "upload"
    imageName = "1_20190718144434.jpg" # учитывай, что этого изображения быть в базе не должно
    testsPath = os.path.join(cfg.APP_PATH, "tests", "res")
    imagePath = os.path.join(testsPath, imageName)
    jsonName = "test.json"
    jsonPath = os.path.join(testsPath, jsonName)

    def addJson(self, files: list, jsonPath):
        files.append(('json', (self.jsonName, open(self.jsonPath, 'rb'), 'application/json')))
        return files

    def addImage(self, files: list):
        files.append(('file', (self.imageName, open(self.imagePath, 'rb'), 'image/jpg')))
        return files

    def test_uploadImageWithInfoUniqueConstrainAreFailure(self):
        files = []
        files = self.addImage(files)
        files = self.addJson(files, self.jsonPath)
        r = requests.post(self.routeUrl, files=files)
        self.assertEqual(500, r.status_code) # это неправильно

    def test_TimeTestInCorrectSituation(self):
        pass

    def test_NoImageHere(self):
        files = []
        files = self.addJson(files, self.jsonPath)
        r = requests.post(self.routeUrl, files=files)
        self.assertNotEqual(200, r.status_code)

    def test_NoJsonHere(self):
        files = []
        files = self.addImage(files)
        r = requests.post(self.routeUrl, files=files)
        self.assertNotEqual(200, r.status_code)

    def test_NoImageNoJson(self):
        files = []
        r = requests.post(self.routeUrl, files=files)
        self.assertNotEqual(200, r.status_code)

    def test_IncorrectJsonImageFilename(self):
        files = []
        jsonPath = os.path.join(cfg.APP_PATH, "res", "incorrectJsonImageFilename.json")
        files = self.addImage(files)
        files = self.addJson(files, jsonPath)
        r = requests.post(self.routeUrl, files=files)
        self.assertNotEqual(200, r.status_code)

    def test_IncorrectJsonImageFixationDatetime(self):
        files = []
        jsonPath = os.path.join(cfg.APP_PATH, "res", "incorrectJsonFixa.json")
        files = self.addImage(files)
        files = self.addJson(files, jsonPath)
        r = requests.post(self.routeUrl, files=files)
        self.assertNotEqual(200, r.status_code)

    def test_IncorrectJsonImageNumberOfCamera(self):
        files = []
        jsonPath = os.path.join(cfg.APP_PATH, "res", "incorrectJsonNumberOfCamera.json")
        files = self.addImage(files)
        files = self.addJson(files, jsonPath)
        r = requests.post(self.routeUrl, files=files)
        self.assertNotEqual(200, r.status_code)

    def test_IncorrectImageFilename(self):
        files = []
        jsonPath = os.path.join(cfg.APP_PATH, "res", "incorrectJsonImageFilename.json")
        files = self.addImage(files)
        files = self.addJson(files, jsonPath)
        r = requests.post(self.routeUrl, files=files)
        self.assertNotEqual(200, r.status_code)

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
