from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Iterable

from django.utils import timezone as dj_tz
from channels.testing import WebsocketCommunicator
from exchange_rate.models import ExchangeRate


class ConnectException(Exception):
    ...


class AuthWebsocketCommunicator(WebsocketCommunicator):
    def __init__(self, application, path, auth=None, headers=None, subprotocols=None):
        super().__init__(application, path, headers, subprotocols)
        self.scope["user"] = auth

    async def __aenter__(self) -> WebsocketCommunicator:
        connected, _ = await self.connect()
        if not connected:
            raise ConnectException("connection failed")
        return self

    async def __aexit__(self, type, value, traceback):
        await self.disconnect()


class BaseTest:
    @staticmethod
    def mock_now(timezone: str = dj_tz.get_current_timezone_name(), **kwargs) -> datetime:
        """
        timezone(str): defulat = django.settings.TIME_ZONE(Asia/Seoul)
        kwargs: `year, month, day, hour, minute, second, microsecond, tzinfo, fold`
        """
        now = datetime.now(ZoneInfo(timezone))
        return now.replace(**kwargs)

    @staticmethod
    def exchange_min_price(country: str, iterable: Iterable[ExchangeRate]) -> ExchangeRate:
        return min(
            filter(lambda y: y.country == country, iterable),
            key=lambda x: x.standard_price,
        )

    @staticmethod
    def exchange_max_price(country: str, iterable: Iterable[ExchangeRate]) -> ExchangeRate:
        return max(
            filter(lambda y: y.country == country, iterable),
            key=lambda x: x.standard_price,
        )

    @staticmethod
    def exchange_last_price(country: str, iterable: Iterable[ExchangeRate]) -> ExchangeRate:
        return max(filter(lambda y: y.country == country, iterable), key=lambda x: x.created_at)
