import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.conf.beat_schedule = {
	'update_exchange_rate': {
		'task': 'exchange_rate.tasks.update_exchange_rate',
		'schedule': crontab(hour='9-16', minute='*/1', day_of_week='1-5'),
	},
}

