import unittest
from config import Config as cfg
import requests


class Gallery(unittest.TestCase):
    routeUrl = cfg.serverUrl + "gallery"

    def test_GetAllImagesNotEmpty(self):
        r = requests.get(self.routeUrl)
        self.assertTrue(r.content)

    def test_GetAllImagesHaveSameElements(self):
        r = requests.get(self.routeUrl)
        self.assertTrue(r.content)


if __name__ == '__main__':
    unittest.main()


