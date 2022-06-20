from datetime import datetime
from zoneinfo import ZoneInfo
from django.utils import timezone as dj_tz
from channels.testing import WebsocketCommunicator



class AuthWebsocketCommunicator(WebsocketCommunicator):
    def __init__(self, application, path, auth=None, headers=None, subprotocols=None):
        super().__init__(application, path, headers, subprotocols)
        self.scope["user"] = auth


class BaseTest():
    @staticmethod
    def mock_now(timezone: str = dj_tz.get_current_timezone_name(), **kwargs) -> datetime:
        """ 
        timezone(str): defulat = django.settings.TIME_ZONE(Asia/Seoul)
        kwargs: `year, month, day, hour, minute, second, microsecond, tzinfo, fold`
        """
        now = datetime.now(ZoneInfo(timezone))
        return now.replace(**kwargs)