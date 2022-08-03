from decimal import Decimal

from django.test import TestCase, TransactionTestCase
from django.contrib.auth import get_user_model

from exchange_rate.models import Country

from .models import Alert
from .query import alert_query

User = get_user_model()


class AlertTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            email="alert@email.com",
            nickname="alert_user",
            gender="male",
            age_range="20~29",
            refresh_token="NULL",
        )
        usd = Country.objects.create(
            name="미국",
            currency="USD",
            currency_kr="달러",
            standard_price=1
        )
        jpy = Country.objects.create(
            name="일본",
            currency="jpy",
            currency_kr="엔",
            standard_price=100
        )
        self.data = [
            Alert(
                user=user,
                country=usd,
                price=100
            ),
            Alert(
                user=user,
                country=usd,
                price=100.1
            ),
            Alert(
                user=user,
                country=usd,
                price=99.9
            ),
            Alert(
                user=user,
                country=jpy,
                price=100
            ),
            Alert(
                user=user,
                country=jpy,
                price=99.9,
                active=False
            ),
            Alert(
                user=user,
                country=jpy,
                price=99.9,
                send=True
            ),
        ]
        Alert.objects.bulk_create(self.data)

    def test_alert_query(self):
        query_set = alert_query(100, "미국")
        self.assertEqual(len(query_set), 2)
        self.assertEqual(query_set[0].price, Decimal(str(100)))
        self.assertEqual(query_set[0].country.name, "미국")
        self.assertEqual(query_set[1].price, Decimal(str(99.90)))
        self.assertEqual(query_set[1].country.name, "미국")

        query_set2 = alert_query(100, "일본")
        self.assertEqual(len(query_set2), 1)
        self.assertEqual(query_set2[0].price, Decimal(str(100)))
        self.assertEqual(query_set2[0].country.name, "일본")


