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
	# 9:00 ~ 15:00
	'update_exchange_rate': {
		'task': 'exchange_rate.tasks.update_exchange_rate',
		'schedule': crontab(hour='9-15', minute='*/5', day_of_week='1-5'),
	},
	# # 15:00 ~ 15:30
	# 'last_update_exchange_rate': {
	# 	'task': 'exchange_rate.tasks.update_exchange_rate',
	# 	'schedule': crontab(hour='15', minute='31-59/2', day_of_week='1-5'),
	# },
	

	'last_update_exchange_rate': {
		'task': 'exchange_rate.tasks.test',
		'schedule': crontab(hour='17', minute='31-59/2', day_of_week='1-5'),
	},
}

