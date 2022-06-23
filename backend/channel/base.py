from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer

from .models import Channel


async def channel_group_send(group_name: str, data: dict, type: str = "base_message"):
    channel_layer = get_channel_layer()

    await channel_layer.group_send(group_name, {"type": type, "data": data})


class BaseWebSocket(AsyncJsonWebsocketConsumer):
    @database_sync_to_async
    def __save_channel_data(self, user, group_name, channel_name) -> None:
        Channel.objects.create(
            user=user, group_name=group_name, channel_name=channel_name
        )

    @database_sync_to_async
    def __delete_channel_data(self, group_name: str, channel_name: str) -> None:
        Channel.objects.get(group_name=group_name, channel_name=channel_name).delete()

    async def connect(self):
        """
        using:
            call the first `await super().connect()` method

        send:
            pydantic:
                await self.send(pydantic.json())
            other:
                await self.send_json()
        """
        self.user = self.scope["user"]
        self.group_name = self.scope["url_route"]["kwargs"]["currency"].upper()

        if not self.user.is_authenticated:
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        # await self.__save_channel_data(self.user, self.group_name, self.channel_name)
        await self.accept()

    # async def disconnect(self, close_code):
    # await self.__delete_channel_data(self.group_name, self.channel_name)
    # await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def base_message(self, event):
        await self.send(event["data"])
