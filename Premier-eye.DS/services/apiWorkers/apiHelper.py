import requests
from requests import Response, Request
from typing import Optional
from pymonad import either
from config.settings import Settings as config


class ApiHelper:
    def request(self, method, url, **reqKArgs):
        req: Response = requests.request(method, url, **reqKArgs)
        if req.status_code != 200:
            print(req.json())
            if config.strongRequestChecking:
                raise Exception(f"[strongRequestChecking] Завершаю работу, запрос вернулся с кодом {req.status_code}.")

            return either.Left(req.json())
        
        return either.Right(req.json())


