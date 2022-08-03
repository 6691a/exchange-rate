from django.db.models import F, Case, When, QuerySet

from .models import Alert


def alert_query(current: float, country: str) -> QuerySet[Alert]:
    return Alert.objects.annotate(
        value_diff=F("price") - current,
        is_alert=Case(
            When(
                value_diff__lte=0,
                then=True
            ),
            default=False
        )
    ).filter(country__name=country, active=True, is_alert=True, send=False)
