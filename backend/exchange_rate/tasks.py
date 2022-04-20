import re
import json
import httpx
from celery import shared_task
from datetime import datetime
from typing import Union
from django.conf import settings

from .models import ExchangeRate

class Currency:
    def get(self) -> Union[dict, None]:
        """
        httpx 200 ok 
            - return dict
        httpx not 200 
            - return None
        """
        r = httpx.get(settings.EXCHANGE_RATE_API_URL)

        if r.status_code != 200:
            return
        
        req = r.text.replace("var exView = ", "")
        req = re.sub(r",(\s)+]", "]", req)
        return json.loads(req)

    def __str_to_datetime(self, str: str, format: str) -> datetime:
        return datetime.strptime(str, format)

    def update(self) -> None:
        res = self.get()
        
        if not res:
            return
            
        res = json.loads(res)
        if not res:
            return

        call_date = self.__str_to_datetime(res.get("날짜"), "%Y년 %m월 %d일 %H:%M")
        for i in res.get("리스트"):
            currency = i.get("통화명")
            sales_rate = i.get("매기준율")
            ExchangeRate.objects.create(call_date=call_date, currency=currency, sales_rate=sales_rate)

@shared_task
def update_exchange_rate():
    c = Currency()
    c.update()


