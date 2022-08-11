from datetime import date, timedelta, datetime
from django.core.cache import cache

from exchange_rate.models import ExchangeRateSchedule


def date_offset(date: date, offset: int) -> date:
    return date - timedelta(days=offset)


def test():
    day_off = cache.get("day_off")
    today = datetime.today().date()

    if not day_off:
        if ExchangeRateSchedule.objects.filter(day_off=today).exists():
            cache.set("day_off", today)
            return True
        cache.set("day_off", -1)
        return False

    if day_off == today:
        return True
    return False

def work_date(date: date) -> date:
    test()
    # cache.set("day_off", -1)
    # if cache.get("day_off"):
    #     print(date_offset(date, -1))
        # work_date(date_offset(date, -1))
        # print(date)
    offset = date.weekday() - 4
    if 0 < offset:
        return date_offset(date, offset)
    return date
