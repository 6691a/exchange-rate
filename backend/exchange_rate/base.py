from datetime import date, timedelta, datetime

from exchange_rate.models import ExchangeRateSchedule


def date_offset(date_time: datetime, offset: int) -> datetime:
    """
    offset:
        - 양수(data - offset)
        - 음수(date + offset)
    """
    return date_time - timedelta(days=offset)


def work_date(date_time: datetime) -> date:
    schedules: list[ExchangeRateSchedule] = ExchangeRateSchedule.objects.filter(
        day_off__range=[date_offset(date_time, 15), date_time]
    ).values_list(
        "day_off",
        flat=True
    )
    date = date_time.date()
    while True:
        if date in schedules:
            date = date_offset(date, 1)
        else:
            if (offset := date.weekday() - 4) > 0:
                date = date_offset(date, offset)
            break
    return date

