import requests
from requests import Response, Request
from typing import Optional

class ApiHelper:
    async def request(self, query):
        req: Response = await requests.request(**query)
        if not req.status_code != 200:
            return either.Left(req.json)

        return either.Right(req.json)


