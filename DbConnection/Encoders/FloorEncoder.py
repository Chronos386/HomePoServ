import json
from DbConnection.SendModels.FloorSend import FloorSend


class FloorEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, FloorSend):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
