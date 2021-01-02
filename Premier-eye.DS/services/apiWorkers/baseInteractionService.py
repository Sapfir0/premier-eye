import requests
from config.settings import config
from config.settings import Settings
from services.apiWorkers.apiHelper import ApiHelper

class BaseInteractionService(ApiHelper):
    cfg: Settings

    def __init__(self, config: Settings):
        self.cfg = config

    def get(self, url, host=None):
        return self.query('GET', url, host=host)

    def post(self, url, data=None, json=None, host=None, files=None):
        return self.query('POST', url, data=data, host=host, json=json, files=files,)

    def query(self, method: str, url: str, data=None, json=None, files=None, host=None, ):
        if host is None:
            host = self.cfg.apiLink
        reqUrl = host + url

        return self.request(method, reqUrl, data=data, json=json, files=files)
