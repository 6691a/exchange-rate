from base.schemas import ResponseSchema, ErrorSchema

from channel.base import BaseWebSocket
from ..apis.v1.schemas import ExchangeRateSchema
from .query import today_exchange


class ExchangeRateConsumer(BaseWebSocket):
    async def connect(self):
        await super().connect()
        print("123123")
        print(await today_exchange(currency__icontains=self.group_name))
        if exchange := await today_exchange(currency__icontains=self.group_name):
            return await self.send(
                ResponseSchema(data=[ExchangeRateSchema(**i.dict) for i in exchange]).json()
            )
        await self.send(
            ResponseSchema(data=ErrorSchema(error="currency not found"), status=400).json()
        )

    async def disconnect(self, close_code):
        super().disconnect(close_code)



