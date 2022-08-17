from .models import Alert
from account.models import User

def get_alert(user: User, country) -> Query:
    return Alert.objects.get(
        user=user,
        active=True,
        country=country,
        send=False
    )
