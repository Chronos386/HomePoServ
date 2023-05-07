import json
from DbConnection.SendModels.SensorSend import SensorSend


class SensorEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SensorSend):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
