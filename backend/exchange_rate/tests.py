from django.test import TestCase
from django.utils import timezone
from channels.testing import HttpCommunicator

from .models import ExchangeRate
from channel.base import channel_group_send
from base.schemas import ResponseSchema
from .apis.v1.schemas import ExchangeRateSchema


class ChannelSendTest(TestCase):
    def setUp(self):
        data = [
            ExchangeRate(fix_time=timezone.now(), currency="USD", country="미국", standard_price=1150),
            ExchangeRate(fix_time=timezone.now(), currency="JPY", country="일본", standard_price=970),
            ExchangeRate(fix_time=timezone.now(), currency="CNY", country="중국", standard_price=190),
            ExchangeRate(fix_time=timezone.now(), currency="GBP", country="영국", standard_price=1590.68),
        ]
        ExchangeRate.objects.bulk_create(data)
    
    # def test_channel_group_send(self):
    #     data = ExchangeRate.objects.all()
    #     for i in data:
    #         print(ResponseSchema(data=(ExchangeRateSchema(**i.dict))).json())
    #         channel_group_send(
    #             group_name=i.currency,
    #             data=ResponseSchema(data=(ExchangeRateSchema(**i.dict))).json()
    #         )

            