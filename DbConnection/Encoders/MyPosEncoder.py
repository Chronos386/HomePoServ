import json
from DbConnection.SendModels.MyPosition import MyPosition


class MyPosEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, MyPosition):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
