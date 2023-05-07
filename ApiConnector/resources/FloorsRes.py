from flask import Response
from ApiConnector.resources.MainRes import MainRes


class FloorsRes(MainRes):
    def get(self):
        floors = self.dbClass.getAllFloorsJSON()
        return Response(floors, mimetype='application/json')
