from __future__ import absolute_import
from .celery import app as celery_app
import django

__all__ = ("celery_app",)

django.setup()
