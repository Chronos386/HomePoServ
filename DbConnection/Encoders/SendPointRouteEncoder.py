import json
from Models.SendRoute import SendRoute
from Models.SendPointRoute import SendPointRoute


class SendRouteEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SendRoute):
            return obj.__dict__
        if isinstance(obj, SendPointRoute):
            return obj.__dict__()
        return json.JSONEncoder.default(self, obj)
