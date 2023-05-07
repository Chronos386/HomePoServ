from flask import Response
from flask_restful import reqparse
from ApiConnector.resources.MainRes import MainRes


class SensorRes(MainRes):
    def get(self, sens_id):
        sensor = self.dbClass.getSensorJSON(sensor_id=sens_id)
        return Response(sensor, mimetype='application/json')

    # создание нового датчика
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("x", type=float)
        parser.add_argument("y", type=float)
        parser.add_argument("z", type=float)
        req = parser.parse_args()
        self.dbClass.addNewSensor(x=req.x, y=req.y, z=req.z)
        return {}, 200

    # обновление существующего датчика
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("sensor_id", type=int)
        parser.add_argument("x", type=float)
        parser.add_argument("y", type=float)
        parser.add_argument("z", type=float)
        req = parser.parse_args()
        self.dbClass.updSensor(sensor_id=req.sensor_id, x=req.x, y=req.y, z=req.z)
        return {}, 200

    # удаление существующего датчика
    def delete(self, sens_id):
        self.dbClass.delSensor(sensor_id=sens_id)
        return {}, 200
