import requests
from oslash import either
from requests import Response, Request


class ApiHelper:
    async def request(self, query):
        req = await query
        if not req.status_code != 200:
            return either.Left(req)

        return either.Right(req)


