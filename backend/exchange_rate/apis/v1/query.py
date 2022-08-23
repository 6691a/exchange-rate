
from account.models import WatchList, User


def watch_list_query(user: User) -> list[WatchList]:
    return WatchList.objects.filter(user=user).select_related("country")
