from unittest.mock import patch

from django.template.loader import render_to_string
from django.test import TestCase, TransactionTestCase
from django.contrib.auth import get_user_model

from base.tests import BaseTest
from exchange_rate.models import ExchangeRate
from exchange_rate.tests import create_exchange, create_country
from .models import Alert
from .query import alert_query

from account.tests import create_user


class AlertTest(TestCase):
    def setUp(self):
        self.user1 = create_user("email1@email.com")
        self.user2 = create_user("email2@email.com")

        self.country_usd = create_country(
            name="미국",
            currency="USD",
            currency_kr="달러",
            standard_price=1
        )
        self.country_jpy = create_country(
            name="일본",
            currency="JPY",
            currency_kr="엔",
            standard_price=100.0
        )

    def test_create_alert(self):
        self.client.force_login(self.user1)
        date = BaseTest.mock_now(year=2022, month=8, day=5)

        self.exchnage_USD = create_exchange(
            date,
            fix_time=date, currency="USD", country="미국", standard_price=1430,
        )
        with patch("exchange_rate.channel.query.datetime") as mock:
            mock.today.return_value = date

            # 계약 등록
            res = self.client.post(
                path="/api/v1/alert/",
                data={
                    "currency": "USD",
                    "price": 1200
                },
                content_type="application/json",
            )
            self.assertEqual(res.status_code, 200)

            self.client.force_login(self.user2)
            res = self.client.post(
                path="/api/v1/alert/",
                data={
                    "currency": "USD",
                    "price": 1500
                },
                content_type="application/json",
            )
            self.assertEqual(res.status_code, 200)


            query_set = alert_query(1500.0, "미국")





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
