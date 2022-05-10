from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from base.models import BaseModel


class ExchangeRate(BaseModel):
    fix_time = models.DateTimeField(verbose_name="환율 갱신일")
    currency = models.CharField(max_length=25, verbose_name="통화")
    sales_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="매매 기준")

    class Meta:
        db_table = "exchange_rate"
        ordering = []


@receiver(post_save, sender=ExchangeRate)
def creat_exchange_rate(sender, instance, created, **kwargs):
    if created:
        print(instance.__dict__)
        # Profile.objects.create(user=instance)


class ExchangeRateSchedule(BaseModel):
    day_off = models.DateField(verbose_name="쉬는 날")
    memo = models.TextField(verbose_name="메모", blank=True, null=True)

    class Meta:
        db_table = "exchange_rate_schedule"
        ordering = []
