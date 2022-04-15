from django.db import models
from base.models import BaseModel

class ExchangeRate(BaseModel):
    currency = models.CharField(max_length=25, verbose_name="통화")
    sales_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="매매 기준")
    class Meta:
        db_table = "exchange_rate"
        ordering = []