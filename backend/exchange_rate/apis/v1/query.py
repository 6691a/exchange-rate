from asgiref.sync import sync_to_async

from account.models import WatchList, User

@sync_to_async
def watch_list_query(user: User) -> list[WatchList]: 
    return list(WatchList.objects.filter(user=user).select_related("country"))