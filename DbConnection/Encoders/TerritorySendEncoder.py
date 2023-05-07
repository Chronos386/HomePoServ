import json
from DbConnection.SendModels.TerritorySend import TerritorySend


class TerritorySendEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, TerritorySend):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
