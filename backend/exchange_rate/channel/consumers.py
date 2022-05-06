from datetime import date
from typing import List
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models.query import QuerySet

from base.schemas import ResponseSchema
from ..apis.v1.schemas import ExchangeRateSchema
from ..models import ExchangeRate


@database_sync_to_async
def today_exchange(*args, **kwargs) -> List:
    kwargs["created_at__date"] = date.today()
    return list(ExchangeRate.objects.filter(*args, **kwargs))


class ExchangeRateConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        """
        using pydantic :
            await self.send(pydantic.json())
        other :
            await self.send_json()
        """
        self.group_name = self.scope["url_route"]["kwargs"]["currency"]
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        if exchange := await today_exchange(currency__icontains=self.group_name):
            print(ExchangeRate.parse_obj(exchange))
            # print(ResponseSchema.parse_obj(data=ExchangeRate(exchange)))

            # data = ResponseSchema(data=List[ExchangeRateSchema(**exchange.dict)])
            # await self.send(data.json())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
