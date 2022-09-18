from datetime import date, timedelta, datetime

from exchange_rate.models import ExchangeRateSchedule


def date_offset(date_time: datetime, offset: int) -> datetime:
    """
    offset:
        - 양수(data - offset)
        - 음수(date + offset)
    """
    return date_time - timedelta(days=offset)


def work_date(date_time: datetime) -> datetime:
    schedules: list[ExchangeRateSchedule] = ExchangeRateSchedule.objects.filter(
        day_off__range=[date_offset(date_time, 15), date_time]
    ).values_list(
        "day_off",
        flat=True
    )

    while True:
        if date_time.date() in schedules:
            date_time = date_offset(date_time, 1)
        else:
            if (offset := date_time.weekday() - 4) > 0:
                date_time = date_offset(date_time, offset)
            break
    return date_time

