from django.db import models
from django.conf import settings

from base.models import BaseModel


class Channel(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=25)
    channel_name = models.CharField(max_length=100)

    class Meta:
        db_table = "channel"
        ordering = []
