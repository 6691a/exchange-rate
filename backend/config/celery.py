import os
from celery import Celery
from .settings.environment import ENV
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", ENV.SETTING_PATH)

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


# local celery beat test
if settings.DEBUG:
    from celery.schedules import crontab

    app.conf.beat_schedule = {
        # "day_off": {
        #     "task": "exchange_rate.tasks.day_off",
        #     "schedule": crontab(hour="8", minute="30", day_of_week="1-5"),
        # },
        # 9:00 ~ 15:00
        "exchange_rate": {
            "task": "exchange_rate.tasks.exchange_rate",
            "schedule": crontab(minute="*/1", day_of_week="1-5"),
        },
        # 15:00 ~ 15:30
        # "_exchange_rate": {
        #     "task": "exchange_rate.tasks.exchange_rate",
        #     "schedule": crontab(hour="15", minute="0-30/5", day_of_week="1-5"),
        # },
    }
