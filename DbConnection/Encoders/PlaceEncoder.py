import json
from DbConnection.SendModels.PlaceSend import PlaceSend


class PlaceEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, PlaceSend):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
