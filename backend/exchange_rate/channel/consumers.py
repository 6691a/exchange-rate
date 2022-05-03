# chat/consumers.py
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ExchangeRateConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        await self.send_json({"test": "text"})
