import requests
from requests import Request
from config.settings import Settings
from dependency_injector import containers, providers


class BaseInteractionService:
    cfg: Settings

    def __init__(self, config: Settings):
        self.cfg = config

    def get(self, url, host=None):
        return self.query('GET', url, host=host )

    def post(self, url, data=None, host=None, files=None):
        return self.query('POST', url, data=data, host=host, files=files,)

    def query(self, method: str, url: str, data=None, files=None, host=None, ):
        if host is None:
            host = "http://localhost:8050" # TODO ааа почему DI не работает
        reqUrl = host + url

        return requests.request(method, reqUrl, data=data, files=files)
