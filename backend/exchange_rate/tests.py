from unittest.mock import patch
from datetime import timedelta
from asgiref.sync import sync_to_async
from django.test import TransactionTestCase, TestCase
from django.contrib.auth import get_user_model
from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack

from base.tests import AuthWebsocketCommunicator, BaseTest
from .base import work_date
from .models import ExchangeRate, ExchangeRateSchedule
from .tasks import update_exchange_rate
from .channel.routing import websocket_urlpatterns

application = AuthMiddlewareStack(URLRouter(websocket_urlpatterns))

User = get_user_model()

SLEEP_TIME = 0.001

#
# class TaskTest(TransactionTestCase):
#     def setUp(self):
#         yester_data = [
#             ExchangeRate(
#                 fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=100
#             ),
#         ]
#         with patch("django.utils.timezone.now") as mock:
#             mock.return_value = BaseTest.mock_now(year=2022, month=8, day=5) - timedelta(1)
#             ExchangeRate.objects.bulk_create(yester_data)
#
#         today_data = [
#             ExchangeRate(
#                 fix_time=BaseTest.mock_now(),
#                 currency="USD",
#                 country="미국",
#                 standard_price=1000,
#             ),
#             ExchangeRate(
#                 fix_time=BaseTest.mock_now(),
#                 currency="USD",
#                 country="미국",
#                 standard_price=1060,
#             ),
#             ExchangeRate(
#                 fix_time=BaseTest.mock_now(),
#                 currency="USD",
#                 country="미국",
#                 standard_price=1120,
#             ),
#             ExchangeRate(
#                 fix_time=BaseTest.mock_now(),
#                 currency="USD",
#                 country="미국",
#                 standard_price=1190,
#             ),
#             ExchangeRate(
#                 fix_time=BaseTest.mock_now(),
#                 currency="USD",
#                 country="미국",
#                 standard_price=990,
#             ),
#         ]
#         with patch("django.utils.timezone.now") as mock:
#             mock.return_value = BaseTest.mock_now(year=2022, month=8, day=5)
#             ExchangeRate.objects.bulk_create(today_data)
#
#         self.user = User.objects.create(
#             email="user@example.com",
#             nickname="user",
#             gender="male",
#             age_range="20~29",
#             avatar_url="None",
#         )
#
#     async def test_update_exchange_rate(self):
#         with patch("exchange_rate.channel.query.date") as mock:
#             mock.today.return_value = BaseTest.mock_now(year=2022, month=8, day=5)
#
#             async with AuthWebsocketCommunicator(
#                 application, "/ws/exchange_rate/USD/", self.user
#             ) as wc:
#                 # connect send pop
#                 await wc.receive_json_from()
#                 query_set = await sync_to_async(ExchangeRate.objects.create)(
#                     fix_time=BaseTest.mock_now(),
#                     currency="USD",
#                     country="미국",
#                     standard_price=900.0,
#                 )
#
#                 await sync_to_async(update_exchange_rate)(query_set)
#
#                 res = await wc.receive_json_from()
#                 res = res["data"]["exchange_rate"][0]
#
#                 self.assertEqual(res["country"], query_set.country)
#                 self.assertEqual(res["standard_price"], query_set.standard_price)
#                 self.assertEqual(res["currency"], query_set.currency)

class BaseCodeTest(TestCase):
    def test_work_date(self):
        ExchangeRateSchedule.objects.create(
            day_off=BaseTest.mock_now(year=2022, month=9, day=9),
            memo="추석"
        )
        ExchangeRateSchedule.objects.create(
            day_off=BaseTest.mock_now(year=2022, month=9, day=12),
            memo="추석"
        )

        print(work_date(BaseTest.mock_now(year=2022, month=9, day=12)))

