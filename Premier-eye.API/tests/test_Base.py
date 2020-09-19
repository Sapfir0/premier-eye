import unittest

from config import Config as cfg
import requests


class Base(unittest.TestCase):

    def test_ServerIsOk(self):
        r = requests.get(cfg.serverUrl)
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()

