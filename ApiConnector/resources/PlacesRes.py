from flask import Response
from flask_restful import reqparse
from ApiConnector.resources.MainRes import MainRes


class PlacesRes(MainRes):
    def get(self):
        places = self.dbClass.getAllPlacesJSON()
        return Response(places, mimetype='application/json; charset=utf-8')

    # создание нового места
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("x", type=float)
        parser.add_argument("y", type=float)
        parser.add_argument("is_class", type=bool)
        parser.add_argument("floor", type=int)
        parser.add_argument("name", type=str)
        parser.add_argument("descr", type=str)
        parser.add_argument("photo", type=str)
        req = parser.parse_args()
        room = self.sensCoordinator.calcRoom(req.x, req.y, req.floor)
        self.dbClass.addNewPlace(x=req.x, y=req.y, room=room, floor=req.floor, name=req.name, descr=req.descr,
                                 photo=req.photo, is_class=req.is_class)
        return {}, 200

    # обновление существующего места
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("place_id", type=float)
        parser.add_argument("x", type=float)
        parser.add_argument("y", type=float)
        parser.add_argument("is_class", type=bool)
        parser.add_argument("floor", type=int)
        parser.add_argument("name", type=str)
        parser.add_argument("descr", type=str)
        parser.add_argument("photo", type=str)
        req = parser.parse_args()
        room = self.sensCoordinator.calcRoom(req.x, req.y, req.floor)
        self.dbClass.updPlace(place_id=req.place_id, x=req.x, y=req.y, room=room, floor=req.floor, name=req.name,
                              descr=req.descr, photo=req.photo, is_class=req.is_class)
        return {}, 200

    # удаление существующего места
    def delete(self, place_id):
        self.dbClass.delPlace(place_id=place_id)
        return {}, 200
