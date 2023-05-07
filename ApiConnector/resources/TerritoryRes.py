from flask import Response
from flask_restful import reqparse
from ApiConnector.resources.MainRes import MainRes


class TerritoryRes(MainRes):
    def get(self):
        territory = self.dbClass.getTerritoryJSON()
        return Response(territory, mimetype='application/json')

    # обновление территории
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("x", type=float)
        parser.add_argument("y", type=float)
        parser.add_argument("z", type=float)
        req = parser.parse_args()
        self.dbClass.updTerritory(x=req.x, y=req.y, z=req.z)
        return {}, 200
