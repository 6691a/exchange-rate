from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')

app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))


app.conf.beat_schedule = {
	'update_exchange_rate': {
		'task': 'update_exchange_rate',
		'schedule': crontab(minute='*/30'),
	},
}