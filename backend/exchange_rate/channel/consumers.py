from abc import abstractmethod
from datetime import date
from typing import List
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from base.schemas import ResponseSchema, ErrorSchema

from channel.base import BaseWebSocket
from ..apis.v1.schemas import ExchangeRateSchema
from ..models import ExchangeRate


@database_sync_to_async
def today_exchange(*args, **kwargs) -> List:
    kwargs["created_at__date"] = date.today()
    return list(ExchangeRate.objects.filter(*args, **kwargs))


class ExchangeRateConsumer(BaseWebSocket):
    async def connect(self):
        await super().connect()
        if exchange := await today_exchange(currency__icontains=self.group_name):
            return await self.send(
                ResponseSchema(data=[ExchangeRateSchema(**i.dict) for i in exchange]).json()
            )
        await self.send(
            ResponseSchema(data=ErrorSchema(error="currency not found"), status=400).json()
        )

    async def disconnect(self, close_code):
        super().disconnect(close_code)




