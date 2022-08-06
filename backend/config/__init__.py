from __future__ import absolute_import
from .settings.environment import ENV
from .celery import app as celery_app
from django.conf import settings
from django import setup




__all__ = ("ENV", "celery_app")

if not settings.DEBUG:
    setup()
