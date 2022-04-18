## testapi/task.py
from celery import shared_task
import json
from httpx import AsyncClient
import re
from .models import ExchangeRate

class Currency:
    """
    사용 후 close 할 것
    1. async with httpx.AsyncClient() as client:
    2. client = httpx.AsyncClient()
       ...
       await client.aclose()
    """
    def __init__(self) -> None:
        self.client = AsyncClient(base_url="")
        self.url = "http://fx.kebhana.com/FER1101M.web"

    async def get(self) -> dict:
        async with self.client:
            r = await self.client.get(self.url)

        req = r.text.replace("var exView = ", "")
        req = re.sub(r",(\s)+]", "]", req)
        return json.loads(req)

    async def update(self) -> None:
        res = await self.get()
        ExchangeRate.objects.create(**res)

@shared_task
def update_exchange_rate():
    c = Currency()
    c.update()

@shared_task
def test():
    print ("Testing exchange rate")
    