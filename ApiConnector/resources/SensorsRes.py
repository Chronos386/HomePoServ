from flask import Response
from ApiConnector.resources.MainRes import MainRes


class SensorsRes(MainRes):
    def get(self):
        sensors = self.dbClass.getAllSensorsJSON()
        return Response(sensors, mimetype='application/json')
