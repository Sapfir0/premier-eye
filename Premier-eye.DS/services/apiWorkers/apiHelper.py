import requests
from requests import Response, Request
from typing import Optional
from config.settings import Settings as config


class ApiHelper:
    def request(self, method, url, **reqKArgs):
        req: Response = requests.request(method, url, **reqKArgs)
        if req.status_code != 200:
            print(req.text())
            if config.strongRequestChecking:
                raise Exception(f"[strongRequestChecking] Завершаю работу, запрос вернулся с кодом {req.status_code}.")
            
            return req.json()
        
        return req.json()


