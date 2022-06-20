from unittest.mock import patch
from django.test import TestCase
from typing import Iterable

from base.tests import BaseTest
from .query import latest_exchange_aggregate, fluctuation_rate
from ..models import ExchangeRate


class ChannelsQueryTest(TestCase):
    def setUp(self) -> None:
        self.MOCK_DATE_2022_06_16 = BaseTest.mock_now(year=2022, month=6, day=16)
        with patch('django.utils.timezone.now', return_value=self.MOCK_DATE_2022_06_16):
            self.MOCK_EXCHAGERATE_2022_06_16 = [
                ExchangeRate(fix_time=BaseTest.mock_now(), currency="JPY", country="일본", standard_price=0),
                ExchangeRate(fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=100),
                ExchangeRate(fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=200),
                ExchangeRate(fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=300),
                ExchangeRate(fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=400),
                ExchangeRate(fix_time=BaseTest.mock_now(), currency="JPY", country="일본", standard_price=500),

            ]
            ExchangeRate.objects.bulk_create(self.MOCK_EXCHAGERATE_2022_06_16)

        self.MOCK_DATE_2022_06_17 = BaseTest.mock_now(year=2022, month=6, day=17)
        with patch('django.utils.timezone.now', return_value=self.MOCK_DATE_2022_06_17):
            self.MOCK_EXCHAGERATE_2022_06_17 = [
                ExchangeRate(fix_time=BaseTest.mock_now(), currency="JPY", country="일본", standard_price=600),
                ExchangeRate(fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=700),
                ExchangeRate(fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=800),
                ExchangeRate(fix_time=BaseTest.mock_now(), currency="JPY", country="일본", standard_price=900),

            ]
            ExchangeRate.objects.bulk_create(self.MOCK_EXCHAGERATE_2022_06_17)

        self.MOCK_DATE_2022_06_20 = BaseTest.mock_now(year=2022, month=6, day=20)
        with patch('django.utils.timezone.now', return_value=self.MOCK_DATE_2022_06_20):
            self.MOCK_EXCHAGERATE_2022_06_20 = [
                ExchangeRate(fix_time=BaseTest.mock_now(), currency="JPY", country="일본", standard_price=1000),
                ExchangeRate(fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=1100),
                ExchangeRate(fix_time=BaseTest.mock_now(), currency="JPY", country="일본", standard_price=1200),
                ExchangeRate(fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=1300),
                ExchangeRate(fix_time=BaseTest.mock_now(), currency="JPY", country="일본", standard_price=1400),
            ]
            ExchangeRate.objects.bulk_create(self.MOCK_EXCHAGERATE_2022_06_20)
    
    def __min_price(self, iterable: Iterable[ExchangeRate]) -> ExchangeRate:
        return min(
                filter(lambda y: y.country == "미국", iterable),
                key=lambda x: x.standard_price
            )

    def __max_price(self, iterable: Iterable[ExchangeRate]) -> ExchangeRate:
        return max(
                filter(lambda y: y.country == "미국", iterable),
                key=lambda x: x.standard_price
            )

    @patch('exchange_rate.channel.query.date')
    async def test_latest_exchange_aggregate(self, mock_date):
        mock_date.today.return_value = self.MOCK_DATE_2022_06_16

        min, max = await latest_exchange_aggregate("USD")
        
        self.assertEqual(
            self.__min_price(self.MOCK_EXCHAGERATE_2022_06_16).standard_price,
            min.standard_price
        )
        self.assertEqual(
            self.__max_price(self.MOCK_EXCHAGERATE_2022_06_16).standard_price,
            max.standard_price
        )
    
    async def test_fluctuation_rate(self):
        with patch("exchange_rate.channel.query.date") as mock:
            mock.today.return_value = self.MOCK_DATE_2022_06_17
            yester, last = await fluctuation_rate("USD")

            self.assertEqual(
                self.__min_price(self.MOCK_EXCHAGERATE_2022_06_16).standard_price,
                yester.standard_price
            )
            self.assertEqual(
                self.__max_price(self.MOCK_EXCHAGERATE_2022_06_17).standard_price,
                last.standard_price
            )
        
        # with patch("exchange_rate.channel.query.date") as mock:
        #     mock.today.return_value = date(2022, 6, 20)
        #     res = await fluctuation_rate("USD")
        
        # with patch("exchange_rate.channel.query.date") as mock:
        #     mock.today.return_value = date(2022, 6, 11)
        #     await fluctuation_rate("USD")
