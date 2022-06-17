from channels.testing import WebsocketCommunicator
from json import loads


class AuthWebsocketCommunicator(WebsocketCommunicator):
    def __init__(self, application, path, auth=None, headers=None, subprotocols=None):
        super().__init__(application, path, headers, subprotocols)
        self.scope["user"] = auth
    
