## testapi/task.py
import re
import json
import httpx
from django.conf import settings
from celery import shared_task

from .models import ExchangeRate

class Currency:
    def get(self) -> dict:
        r = httpx.get(settings.EXCHANGE_RATE_API_URL)
        req = r.text.replace("var exView = ", "")
        req = re.sub(r",(\s)+]", "]", req)
        return json.loads(req)

    def update(self) -> None:
        print("111111")
        res = self.get()
        print(res)
        print("12312312312312")
        ExchangeRate.objects.create(**res)

@shared_task
def update_exchange_rate():
    c = Currency()
    print("123123")
    c.update()

