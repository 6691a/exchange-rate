from datetime import date, timedelta, datetime

from exchange_rate.models import ExchangeRateSchedule


def date_offset(date: date, offset: int) -> date:
    """
    offset:
        - 양수(data - offset)
        - 음수(date + offset)
    """
    return date - timedelta(days=offset)


def work_date(date: date) -> date:
    schedule: list[ExchangeRateSchedule] = ExchangeRateSchedule.objects.filter(
        day_off__range=[date_offset(date, 15), date]
    ).values_list(
        "day_off",
        flat=True
    )

    res = date
    while True:
        if res in schedule:
            res = date_offset(res, 1)
            if (offset := res.weekday() - 4) > 0:
                res = date_offset(res, offset)
        else:
            break
    return res


