from django.db import models
from django.conf import settings

from base.models import BaseModel


class ExchangeRate(BaseModel):
    fix_time = models.DateTimeField(verbose_name="환율 갱신일")
    country = models.CharField(max_length=25, verbose_name="국가", default="None")
    currency = models.CharField(max_length=25, verbose_name="통화 단위", default="None")
    standard_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="매매 기준"
    )

    class Meta:
        db_table = "exchange_rate"
        ordering = ["created_at"]


class ExchangeRateSchedule(BaseModel):
    day_off = models.DateField(verbose_name="쉬는 날")
    memo = models.TextField(verbose_name="메모", blank=True, null=True)

    class Meta:
        db_table = "exchange_rate_schedule"
        ordering = []


class Country(BaseModel):
    name = models.CharField(max_length=25, verbose_name="국가")
    currency = models.CharField(max_length=25, verbose_name="통화 단위")
    currency_kr = models.CharField(
        max_length=25, verbose_name="한글 통화 단위", default="null"
    )
    standard_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="매매 기준", default="1"
    )

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        db_table = "country"


class WatchList(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="watch_list",
        verbose_name="사용자",
    )
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="국가")

    def __str__(self):
        return f"{self.user.email}"

    class Meta:
        db_table = "watch_list"
        ordering = []