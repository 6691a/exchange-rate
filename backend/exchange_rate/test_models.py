from unittest.mock import patch
from datetime import datetime
from .models import ExchangeRate, Country


def create_exchange(datetime: datetime, **kwargs) -> ExchangeRate:
    with patch("django.utils.timezone.now") as mock:
        mock.return_value = datetime
        return ExchangeRate.objects.create(**kwargs)

def create_country(**kwargs) -> Country:
    return Country.objects.create(**kwargs)