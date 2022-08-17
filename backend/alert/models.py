from typing import Optional

from django.db import models

from base.models import BaseModel
from exchange_rate.models import Country
from django.contrib.auth import get_user_model

USER = get_user_model()


class BaseAlert(BaseModel):
    """
    abstract model class 주의사항
    https://docs.djangoproject.com/en/4.0/topics/db/models/#be-careful-with-related-name-and-related-query-name
    """
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="%(class)s", verbose_name="사용자")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="%(class)s", verbose_name="알림 국가")
    active = models.BooleanField(default=True, verbose_name="활성화")

    class Meta:
        abstract = True

class AlertManager(models.Manager):
    """
    price 값은 검사에 포함하지 않음
    """
    def get_or_create(self, *, price: int, **kwargs) -> "Alert":
        try:
            query_set: Alert = self.model.objects.get(**kwargs)
        except self.model.DoesNotExist:
            query_set: Alert = self.model.objects.create(price=price, **kwargs)
        return query_set

    def get_object_or_none(self, **kwargs) -> Optional["Alert"]:
        try:
            query_set: Alert | None = self.model.objects.get(**kwargs)
        except self.model.DoesNotExist:
            query_set: Alert | None = None
        return query_set


class Alert(BaseAlert):
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="알림 가격", blank=True
    )
    send = models.BooleanField(default=False, verbose_name="발송 여부")
    objects = AlertManager()

    class Meta:
        db_table = "alert"


class Alert_beat(BaseAlert):
    alert_date = models.DateTimeField(verbose_name="알림 할 시간")
    one_off = models.BooleanField(default=False, verbose_name="일회성")

    class Meta:
        db_table = "alert_beat"
