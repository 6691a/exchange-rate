from __future__ import absolute_import
from .celery import app as celery_app
from django.conf import settings
import django

__all__ = ("celery_app",)

if not settings.DEBUG:
    django.setup()
