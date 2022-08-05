from django.db.models import F, Case, When, QuerySet, ExpressionWrapper, FloatField

from .models import Alert


def alert_query(price: float, country: str) -> QuerySet[Alert]:
    return Alert.objects.annotate(
        value_diff=ExpressionWrapper(F("price") - price, output_field=FloatField()),
        is_alert=Case(
            When(
                value_diff__lte=0,
                then=True
            ),
            default=False
        )
    ).filter(
        country__name=country, active=True, is_alert=True, send=False
    ).select_related("user")

