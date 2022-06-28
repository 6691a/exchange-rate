from celery import shared_task

from .models import WatchList


@shared_task
def insert_watch_list(**kwargs) -> int:
    watch, _ = WatchList.objects.get_or_create(**kwargs)
    return watch.id
