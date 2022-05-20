from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from asgiref.sync import async_to_sync

from base.models import BaseModel
from base.schemas import ResponseSchema
from channel.base import channel_group_send
from .apis.v1.schemas import ExchangeRateSchema


class ExchangeRate(BaseModel):
    fix_time = models.DateTimeField(verbose_name="환율 갱신일")
    currency = models.CharField(max_length=25, verbose_name="통화")
    standard_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="매매 기준")

    class Meta:
        db_table = "exchange_rate"
        ordering = []


@receiver(post_save, sender=ExchangeRate)
def creat_exchange_rate(sender, instance, created, **kwargs):
    if created:
        print(instance.currency)
        async_to_sync(channel_group_send)(group_name="USD", data=ResponseSchema(data=ExchangeRateSchema(**instance.dict)).json())
        print("123")


class ExchangeRateSchedule(BaseModel):
    day_off = models.DateField(verbose_name="쉬는 날")
    memo = models.TextField(verbose_name="메모", blank=True, null=True)

    class Meta:
        db_table = "exchange_rate_schedule"
        ordering = []
