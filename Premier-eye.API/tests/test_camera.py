import unittest
from config import Config as cfg
import requests


class Camera(unittest.TestCase):
    routeUrl = cfg.serverUrl + "gallery/camera"

    camerasList = [1,2,3]

    def test_IsAllCamerasAvailable(self):
        for camera in self.camerasList:
            r = requests.get(f"{self.routeUrl}/{camera}")
            self.assertEqual(200, r.status_code)


if __name__ == '__main__':
    unittest.main()



