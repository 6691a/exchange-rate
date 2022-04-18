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
	# 'update_exchange_rate': {
	# 	'task': 'update_exchange_rate',
	# 	'schedule': crontab(minute='*/30'),
	# },
	'test_code': {
		'task': 'exchange_rate.task.test',
		# 'schedule': crontab(minute='*/30'),
		'schedule': 5,
	},
}

