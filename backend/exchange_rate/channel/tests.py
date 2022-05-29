from unittest.mock import patch
from django.test import TestCase
from django.utils import timezone
from datetime import date

from ..models import ExchangeRate
from .query import latest_exchange_aggregate, latest_date

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

    @patch("exchange_rate.channel.query.latest_date", date.today)
    async def test_latest_exchange_aggregate(self):
        min, max = await latest_exchange_aggregate("USD")
        self.assertEqual(990, min.standard_price)
        self.assertEqual(1190, max.standard_price)




