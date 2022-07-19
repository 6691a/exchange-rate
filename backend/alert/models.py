from django.db import models


class alert(models.Model):
    active = models.BooleanField(default=True)
    send = models.BooleanField(default=False)
