from base.schemas import ResponseSchema, ErrorSchema

from channel.base import BaseWebSocket
from .schemas import ExchangeRateSchema, ChartSchema
from .query import latest_exchange, latest_exchange_aggregate


class ExchangeRateConsumer(BaseWebSocket):
    async def connect(self):
        await super().connect()
        currency = self.group_name.upper()
        if exchange := await latest_exchange(currency__icontains=currency):
            low, high = await latest_exchange_aggregate(currency=currency)
            return await self.send(
                ResponseSchema(
                    data=ChartSchema(
                        exchange_rate=[ExchangeRateSchema(**i.dict) for i in exchange],
                        hight_price=ExchangeRateSchema(**high.dict),
                        low_price=ExchangeRateSchema(**low.dict)
                    ),
                ).json()
            )
        await self.send(
            ResponseSchema(data=ErrorSchema(error="currency not found"), status=400).json()
        )

    async def disconnect(self, close_code):
        super().disconnect(close_code)


from channels.generic.websocket import AsyncJsonWebsocketConsumer
class TestConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(
            dict(a="123")
        )
