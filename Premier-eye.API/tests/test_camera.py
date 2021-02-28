import unittest
from config import Config as cfg
import requests


namespace = '/camera'

class Camera(unittest.TestCase):
    routeUrl = cfg.serverUrl + "/camera"

    camerasList = [1, 2, 3]

    # def getAllImagesFromCamera(self):
    #     for camera in self.camerasList:
    #         r = requests.get(f'{camera}/images')

    # def getCameraList(self):
    #     r = requests.get(f'/list')

    # def getCamera(self):
    #     for camera in self.camerasList:
    #         r = requests.get(f'{camera}/')
    # def test_IsAllCamerasAvailable(self):
    #     for camera in self.camerasList:
    #         r = requests.get(f"{self.routeUrl}/{camera}")
    #         self.assertEqual(200, r.status_code)


if __name__ == '__main__':
    unittest.main()



