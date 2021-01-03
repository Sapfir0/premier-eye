import requests
from requests import Response, Request
from typing import Optional
from config.settings import Settings as config


class ApiHelper:
    def request(self, method, url, **reqKArgs):
        res: Response = requests.request(method, url, **reqKArgs)
        if res.status_code != 200:
            if (res.status_code == None):
                raise Exception("API not found")
            
            print(res.text)
            if config.strongRequestChecking:
                raise Exception(f"[strongRequestChecking] Завершаю работу, запрос вернулся с кодом {res.status_code}.")
            
            return res.json()

        print(res.json())
        return res.json()


