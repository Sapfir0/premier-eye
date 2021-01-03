import requests
from requests import Response, Request
from typing import Optional
from config.settings import Settings as config


class ApiHelper:
    def request(self, method, url, **reqKArgs):
        res: Response = requests.request(method, url, **reqKArgs)
   
        if res.status_code != 200:               
            if config.strongRequestChecking:
                raise Exception(f"[strongRequestChecking] Завершаю работу, запрос вернулся с кодом {res.status_code}.")
        
        try:
            print(res.json())
        except: # произойдет если, например, в ответе будет хтмл или еще что-то не похожее на джсон
            print(res.text)
            raise Exception("Ошибка при запросе, неожиданный ответ(см выше)")

        return res.json()


