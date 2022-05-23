from django.db import models

from base.models import BaseModel


class ExchangeRate(BaseModel):
    fix_time = models.DateTimeField(verbose_name="환율 갱신일")
    country = models.CharField(max_length=25, verbose_name="국가", default="None")
    currency = models.CharField(max_length=25, verbose_name="통화명", default="None")
    standard_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="매매 기준")

    class Meta:
        db_table = "exchange_rate"
        ordering = []


class ExchangeRateSchedule(BaseModel):
    day_off = models.DateField(verbose_name="쉬는 날")
    memo = models.TextField(verbose_name="메모", blank=True, null=True)

    class Meta:
        db_table = "exchange_rate_schedule"
        ordering = []
