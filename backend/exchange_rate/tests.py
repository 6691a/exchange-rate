from unittest.mock import patch

from asgiref.sync import sync_to_async
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack

from base.tests import AuthWebsocketCommunicator
from .models import ExchangeRate
from .tasks import send_exchange_rate
from .channel.routing import websocket_urlpatterns

application = AuthMiddlewareStack(URLRouter(websocket_urlpatterns))

User = get_user_model()

class TaskTest(TestCase):
    def setUp(self):
        data = [
            ExchangeRate(fix_time=timezone.now(), currency="USD", country="미국", standard_price=1000),
            ExchangeRate(fix_time=timezone.now(), currency="USD", country="미국", standard_price=1060),
            ExchangeRate(fix_time=timezone.now(), currency="USD", country="미국", standard_price=1120),
            ExchangeRate(fix_time=timezone.now(), currency="USD", country="미국", standard_price=1190),            
            ExchangeRate(fix_time=timezone.now(), currency="USD", country="미국", standard_price=990),
        ]
        ExchangeRate.objects.bulk_create(data)
        self.user = User.objects.create(
            email="user@example.com",
            nickname="user",
            gender="male",
            age_range="20~29",
            avatar_url="None",
        )

    async def test_send_exchange_rate(self):

        communicator = AuthWebsocketCommunicator(application, "/ws/exchange_rate/USD/", self.user)
        connected, _ = await communicator.connect()

        self.assertTrue(connected)
        
        # connect send pop
        await communicator.receive_json_from()

        data = await sync_to_async(ExchangeRate.objects.create)(fix_time=timezone.now(), currency="USD", country="미국", standard_price=900.0)
        await sync_to_async(send_exchange_rate)(data)

        res = await communicator.receive_json_from()        
        res = res["data"]["exchange_rate"][0]

        self.assertEqual(res["country"], data.country)
        self.assertEqual(res["standard_price"], data.standard_price)
        self.assertEqual(res["currency"], data.currency)

        await communicator.disconnect()

    # def test_group_send(self):
    #     ...


