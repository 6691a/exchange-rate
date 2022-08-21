from decimal import Decimal

from django.template.loader import render_to_string
from django.test import TestCase, TransactionTestCase
from django.contrib.auth import get_user_model

from base.tests import BaseTest
from exchange_rate.models import Country, ExchangeRate

from .models import Alert
from .query import alert_query

User = get_user_model()


class AlertTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="alert@email.com",
            nickname="alert_user",
            gender="male",
            age_range="20~29",
            refresh_token="NULL",
        )
        self.country_usd = Country.objects.create(
            name="미국",
            currency="USD",
            currency_kr="달러",
            standard_price=1
        )
        self.country_jpy = Country.objects.create(
            name="일본",
            currency="jpy",
            currency_kr="엔",
            standard_price=100.0
        )

    def test_alert_query(self):
        self.data = [
            Alert(
                user=self.user,
                country=self.country_usd,
                price=100.0
            ),
            Alert(
                user=self.user,
                country=self.country_usd,
                price=100.1
            ),
            Alert(
                user=self.user,
                country=self.country_usd,
                price=99.9
            ),
            Alert(
                user=self.user,
                country=self.country_jpy,
                price=100.0
            ),
            Alert(
                user=self.user,
                country=self.country_jpy,
                price=99.9,
                active=False
            ),
            Alert(
                user=self.user,
                country=self.country_jpy,
                price=99.9,
                send=True
            ),
        ]
        self.objects = Alert.objects.bulk_create(self.data)

        query_set = alert_query(100.0, "미국")
        self.assertEqual(len(query_set), 2)
        self.assertEqual(float(query_set[0].price), 100)
        self.assertEqual(query_set[0].country.name, "미국")
        self.assertEqual(float(query_set[1].price), 99.90)
        self.assertEqual(query_set[1].country.name, "미국")

        query_set2 = alert_query(100.0, "일본")
        self.assertEqual(len(query_set2), 1)
        self.assertEqual(float(query_set2[0].price), 100)
        self.assertEqual(query_set2[0].country.name, "일본")

    def test_alert_msg(self):
        query_set: ExchangeRate = ExchangeRate.objects.create(
            fix_time=BaseTest.mock_now(), currency="USD", country="미국", standard_price=100
        )
        msg = render_to_string(
            "kakao/alert.txt", {"name": f"{query_set.country}({query_set.currency})", "price": query_set.standard_price}
        )
        url = f"https://finance.1ife.kr/{query_set.currency.upper()}"

        self.assertIn(
            f"{query_set.country}({query_set.currency}) {query_set.standard_price}원",
            msg
        )
        self.assertEqual(url, "https://finance.1ife.kr/USD")
