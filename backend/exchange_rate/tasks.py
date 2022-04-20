## testapi/task.py
import re
import json
from django.conf import settings
from celery import shared_task
from httpx import AsyncClient

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
        self.url = settings.EXCHANGE_RATE_API_URL

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
