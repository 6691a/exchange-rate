from datetime import date
from typing import List
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from base.schemas import ResponseSchema, ErrorSchema
from channel.models import Channel
from ..apis.v1.schemas import ExchangeRateSchema
from ..models import ExchangeRate


@database_sync_to_async
def today_exchange(*args, **kwargs) -> List:
    kwargs["created_at__date"] = date.today()
    return list(ExchangeRate.objects.filter(*args, **kwargs))


@database_sync_to_async
def save_channel_data(user, group_name, channel_name) -> None:
    Channel.objects.create(user=user, group_name=group_name, channel_name=channel_name)


@database_sync_to_async
def delete_channel_data(group_name, channel_name) -> None:
    Channel.objects.get(group_name=group_name, channel_name=channel_name).delete()


class ExchangeRateConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        """
        using pydantic :
            await self.send(pydantic.json())
        other :
            await self.send_json()
        """
        user = self.scope["user"]
        self.group_name = self.scope["url_route"]["kwargs"]["currency"]

        if not user.is_authenticated:
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await save_channel_data(user, self.group_name, self.channel_name)
        await self.accept()

        if exchange := await today_exchange(currency__icontains=self.group_name):
            return await self.send(
                ResponseSchema(data=[ExchangeRateSchema(**i.dict) for i in exchange]).json()
            )
        await self.send(
            ResponseSchema(data=ErrorSchema(error="currency not found"), status=400).json()
        )

    async def disconnect(self, close_code):
        await delete_channel_data(self.group_name, self.channel_name)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
