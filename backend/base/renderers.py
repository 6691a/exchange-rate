from ninja.renderers import BaseRenderer
import json


class Response(BaseRenderer):
    media_type = "application/json"

    def render(self, request, data, *, response_status):
        data = {"data": data, "status": response_status}
        return json.dumps(data, default=str)
