from flask import Response
from flask_restful import reqparse
from ApiConnector.resources.MainRes import MainRes


class FloorRes(MainRes):
    def get(self, floor):
        sendFloor = self.dbClass.getFloorJSON(floor=floor)
        return Response(sendFloor, mimetype='application/json')

    # создание нового этажа
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("z_start", type=float)
        parser.add_argument("z_end", type=float)
        parser.add_argument("floor", type=int)
        parser.add_argument("photo", type=str)
        req = parser.parse_args()
        self.dbClass.addNewFloor(z_start=req.z_start, z_end=req.z_end, floor=req.floor, photo=req.photo)
        return {}, 200

    # обновление фото этажа
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("floor", type=int)
        parser.add_argument("photo", type=str)
        req = parser.parse_args()
        self.dbClass.updFloorPhoto(floor=req.floor, photo=req.photo)
        return {}, 200

    # удаление этажа
    def delete(self, floor):
        self.dbClass.delFloor(floor=floor)
        return {}, 200
