from django.test import TestCase
from django.utils import timezone

from ..models import ExchangeRate
from .query import today_exchange_aggregate


class ChannelQueryTest(TestCase):
    def setUp(self) -> None:
        data = [
            ExchangeRate(fix_time=timezone.now(), currency="USD", country="미국", standard_price=1000),
            ExchangeRate(fix_time=timezone.now(), currency="USD", country="미국", standard_price=1060),
            ExchangeRate(fix_time=timezone.now(), currency="USD", country="미국", standard_price=1120),
            ExchangeRate(fix_time=timezone.now(), currency="USD", country="미국", standard_price=1190),
            ExchangeRate(fix_time=timezone.now(), currency="USD", country="미국", standard_price=990),
        ]
        ExchangeRate.objects.bulk_create(data)

    async def test_today_exchange_aggregate(self):
        min, max = await today_exchange_aggregate("USD")
        self.assertEqual(990, min.standard_price)
        self.assertEqual(1190, max.standard_price)




