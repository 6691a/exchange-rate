from unittest.mock import patch
from django.test import TestCase
from django.utils import timezone
from datetime import date, datetime

from .query import latest_exchange_aggregate, fluctuation_rate

from ..models import ExchangeRate


class ChannelsQueryTest(TestCase):
    def setUp(self) -> None:
        data = [
            ExchangeRate(fix_time=timezone.now(), currency="USD", country="미국", standard_price=1000),
            ExchangeRate(fix_time=timezone.now(), currency="USD", country="미국", standard_price=1060),
            ExchangeRate(fix_time=timezone.now(), currency="USD", country="미국", standard_price=1120),
            ExchangeRate(fix_time=timezone.now(), currency="USD", country="미국", standard_price=1190),
            ExchangeRate(fix_time=timezone.now(), currency="USD", country="미국", standard_price=990),
        ]
        ExchangeRate.objects.bulk_create(data)

    @patch("exchange_rate.channel.query.date", date.today())
    async def test_latest_exchange_aggregate(self):
        min, max = await latest_exchange_aggregate("USD")
        self.assertEqual(990, min.standard_price)
        self.assertEqual(1190, max.standard_price)
    
    async def test_fluctuation_rate(self):
        with patch("exchange_rate.channel.query.date") as mock:
            mock.today.return_value = date(2022, 6, 10)
            await fluctuation_rate("USD")
        
        # with patch("exchange_rate.channel.query.date") as mock:
        #     mock.today.return_value = date(2022, 6, 12)
        #     await fluctuation_rate("USD")
        
        # with patch("exchange_rate.channel.query.date") as mock:
        #     mock.today.return_value = date(2022, 6, 11)
        #     await fluctuation_rate("USD")