from datetime import date
from typing import List
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from base.schemas import ResponseSchema, ErrorSchema
from ..apis.v1.schemas import ExchangeRateSchema
from ..models import ExchangeRate


@database_sync_to_async
def today_exchange(*args, **kwargs) -> List:
    # kwargs["created_at__date"] = date.today()
    kwargs["created_at__date"] = "2022-05-06"

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
            return await self.send(
                ResponseSchema(data=[ExchangeRateSchema(**i.dict) for i in exchange]).json()
            )
        await self.send(
            ResponseSchema(data=ErrorSchema(error="currency not found"), status=400).json()
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
