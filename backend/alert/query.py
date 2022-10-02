from django.db.models import Q, Case, When, QuerySet, ExpressionWrapper, BooleanField

from .models import Alert


def alert_query(price: float, country: str) -> QuerySet[Alert]:
    return Alert.objects.annotate(
        is_alert=Case(
            When(
                range=Alert.RANGE_CHOICE[0][0],
                then=ExpressionWrapper(Q(price__lt=price), output_field=BooleanField())
            ),
            default=ExpressionWrapper(Q(price__gt=price), output_field=BooleanField())
        ),

    ).filter(
        country__name=country, active=True, is_alert=True, send=False
    ).select_related("user")

