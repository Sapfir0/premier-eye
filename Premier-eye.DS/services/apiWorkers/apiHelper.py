import requests
from requests import Response, Request
from typing import Optional
from pymonad import either


class ApiHelper:
    async def request(self, *reqArgs, **reqKArgs):
        req: Response = await requests.request(reqArgs, reqKArgs)
        if not req.status_code != 200:
            print(req.json())
            if config.strongRequestChecking:
                raise Exception(f"[strongRequestChecking] Завершаю работу, запрос вернулся с кодом {req.status_code}.")

            return either.Left(req.json())

        return either.Right(req.json())


