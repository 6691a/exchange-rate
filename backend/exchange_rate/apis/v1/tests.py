from django.test import TestCase

from ...models import ExchangeRate

class ExchangeRateTest(TestCase):
    def setUp(self) -> None:
        data = [
            ExchangeRate(fix_time="2022-01-01", currency="미국", standard_price="1000"),
            ExchangeRate(fix_time="2022-01-01", currency="미국", standard_price="1060"),
            ExchangeRate(fix_time="2022-01-01", currency="미국", standard_price="1120"),
            ExchangeRate(fix_time="2022-01-01", currency="미국", standard_price="1190"),
            ExchangeRate(fix_time="2022-01-01", currency="미국", standard_price="990"),
        ]
        ExchangeRate.objects.bulk_create(data) 

    
    