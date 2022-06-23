from unittest.mock import patch
from django.test import TestCase
from time import sleep
from datetime import timedelta

from django.contrib.auth import get_user_model
from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack

from base.tests import BaseTest, AuthWebsocketCommunicator
from .routing import websocket_urlpatterns
from .query import latest_exchange_aggregate, fluctuation_rate, closing_price
from ..models import ExchangeRate

application = AuthMiddlewareStack(URLRouter(websocket_urlpatterns))

User = get_user_model()

SLEEP_TIME = 0.001


class ChannelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="user@example.com",
            nickname="user",
            gender="male",
            age_range="20~29",
            avatar_url="None",
        )
        self.yester_data = [
            ExchangeRate(
                fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=100
            ),
            ExchangeRate(
                fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=106
            ),
            ExchangeRate(
                fix_time=BaseTest.mock_now(), currency="JPY", country="일본", standard_price=10
            ),
            ExchangeRate(
                fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=112
            ),
            ExchangeRate(
                fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=119
            ),
            ExchangeRate(
                fix_time=BaseTest.mock_now(), currency="JPY", country="일본", standard_price=0
            ),
            ExchangeRate(
                fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=99
            ),
        ]
        with patch("django.utils.timezone.now") as mock:
            for i in self.yester_data:
                mock.return_value = BaseTest.mock_now() - timedelta(1)
                sleep(SLEEP_TIME)
                ExchangeRate.objects.create(**i.dict)

        self.today_data = [
            ExchangeRate(
                fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=1000
            ),
            ExchangeRate(
                fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=1060
            ),
            ExchangeRate(
                fix_time=BaseTest.mock_now(), currency="JPY", country="일본", standard_price=10
            ),
            ExchangeRate(
                fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=1120
            ),
            ExchangeRate(
                fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=1190
            ),
            ExchangeRate(
                fix_time=BaseTest.mock_now(), currency="JPY", country="일본", standard_price=0
            ),
            ExchangeRate(
                fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=990
            ),
        ]
        ExchangeRate.objects.bulk_create(self.today_data)

    async def test_connect_msg(self):
        async with AuthWebsocketCommunicator(
            application, "/ws/exchange_rate/USD/", self.user
        ) as wc:
            res = await wc.receive_json_from()
            self.assertEqual(200, res.get("status"))

            res = res.get("data")
            exchage = res.get("exchange_rate")
            hight = res.get("hight_price")
            low = res.get("low_price")
            closing = res.get("closing_price")

            exchage_answer = list(filter(lambda i: i.country == "미국", self.today_data))
            hight_answer = BaseTest.exchange_max_price("미국", self.today_data)
            low_answer = BaseTest.exchange_min_price("미국", self.today_data)
            closing_answer = self.yester_data[-1]

            for i in range(len(exchage_answer)):
                self.assertEqual(exchage_answer[i].standard_price, exchage[i].get("standard_price"))
                self.assertEqual(exchage_answer[i].country, exchage[i].get("country"))

            self.assertEqual(hight_answer.standard_price, hight.get("standard_price"))
            self.assertEqual(hight_answer.country, hight.get("country"))
            self.assertEqual(low_answer.standard_price, low.get("standard_price"))
            self.assertEqual(low_answer.country, low.get("country"))
            self.assertEqual(closing_answer.standard_price, closing.get("standard_price"))
            self.assertEqual(closing_answer.country, closing.get("country"))


class ChannelsQueryTest(TestCase):
    def setUp(self):
        with patch("django.utils.timezone.now") as mock:
            self.MOCK_EXCHAGERATE_2022_06_16 = [
                ExchangeRate(
                    fix_time=BaseTest.mock_now(), currency="JPY", country="일본", standard_price=0
                ),
                ExchangeRate(
                    fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=100
                ),
                ExchangeRate(
                    fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=200
                ),
                ExchangeRate(
                    fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=300
                ),
                ExchangeRate(
                    fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=400
                ),
                ExchangeRate(
                    fix_time=BaseTest.mock_now(), currency="JPY", country="일본", standard_price=500
                ),
            ]
            for i in self.MOCK_EXCHAGERATE_2022_06_16:
                mock.return_value = BaseTest.mock_now(year=2022, month=6, day=16)
                sleep(SLEEP_TIME)
                ExchangeRate.objects.create(**i.dict)

        with patch("django.utils.timezone.now") as mock:
            self.MOCK_EXCHAGERATE_2022_06_17 = [
                ExchangeRate(
                    fix_time=BaseTest.mock_now(), currency="JPY", country="일본", standard_price=600
                ),
                ExchangeRate(
                    fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=700
                ),
                ExchangeRate(
                    fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=800
                ),
                ExchangeRate(
                    fix_time=BaseTest.mock_now(), currency="JPY", country="일본", standard_price=900
                ),
            ]
            for i in self.MOCK_EXCHAGERATE_2022_06_17:
                mock.return_value = BaseTest.mock_now(year=2022, month=6, day=17)
                sleep(SLEEP_TIME)
                ExchangeRate.objects.create(**i.dict)

        with patch("django.utils.timezone.now") as mock:
            self.MOCK_EXCHAGERATE_2022_06_20 = [
                ExchangeRate(
                    fix_time=BaseTest.mock_now(), currency="JPY", country="일본", standard_price=1000
                ),
                ExchangeRate(
                    fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=1100
                ),
                ExchangeRate(
                    fix_time=BaseTest.mock_now(), currency="JPY", country="일본", standard_price=1200
                ),
                ExchangeRate(
                    fix_time=BaseTest.mock_now(), currency="JPY", country="일본", standard_price=1300
                ),
                ExchangeRate(
                    fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=1300
                ),
                ExchangeRate(
                    fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=1400
                ),
            ]
            for i in self.MOCK_EXCHAGERATE_2022_06_20:
                mock.return_value = BaseTest.mock_now(year=2022, month=6, day=20)
                sleep(SLEEP_TIME)
                ExchangeRate.objects.create(**i.dict)

    @patch("exchange_rate.channel.query.date")
    async def test_latest_exchange_aggregate(self, mock_date):
        mock_date.today.return_value = BaseTest.mock_now(year=2022, month=6, day=16)

        min, max = await latest_exchange_aggregate("USD")

        min_answer = BaseTest.exchange_min_price("미국", self.MOCK_EXCHAGERATE_2022_06_16)
        max_answer = BaseTest.exchange_max_price("미국", self.MOCK_EXCHAGERATE_2022_06_16)

        self.assertEqual(min_answer.standard_price, min.standard_price)
        self.assertEqual(max_answer.standard_price, max.standard_price)

    async def test_fluctuation_rate(self):
        with patch("exchange_rate.channel.query.date") as mock:
            mock.today.return_value = BaseTest.mock_now(year=2022, month=6, day=17)
            yester, last = await fluctuation_rate("USD")

            yester_answer = BaseTest.exchange_max_price("미국", self.MOCK_EXCHAGERATE_2022_06_16)
            last_answer = BaseTest.exchange_max_price("미국", self.MOCK_EXCHAGERATE_2022_06_17)

            self.assertEqual(yester_answer.standard_price, yester.standard_price)
            self.assertEqual(last_answer.standard_price, last.standard_price)

        with patch("exchange_rate.channel.query.date") as mock:
            mock.today.return_value = BaseTest.mock_now(year=2022, month=6, day=20)
            yester, last = await fluctuation_rate("USD")

            yester_answer = BaseTest.exchange_max_price("미국", self.MOCK_EXCHAGERATE_2022_06_17)
            last_answer = BaseTest.exchange_max_price("미국", self.MOCK_EXCHAGERATE_2022_06_20)

            self.assertEqual(yester_answer.standard_price, yester.standard_price)
            self.assertEqual(last_answer.standard_price, last.standard_price)

    # async def test_closing_price(self):
    #     with patch(
    #         "exchange_rate.channel.query._work_date",
    #         return_value=BaseTest.mock_now(year=2022, month=6, day=20),
    #     ):
    #         closing = await closing_price("USD")
    #         print(closing)
    # closing_answer = BaseTest.exchange_max_price("미국", self.MOCK_EXCHAGERATE_2022_06_20)

    #         self.assertEqual(closing_answer.standard_price, closing.standard_price)
