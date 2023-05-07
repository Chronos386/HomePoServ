import json
from flask import Response
from flask_restful import reqparse
from Models.SendRoute import SendRoute
from ApiConnector.resources.MainRes import MainRes
from DbConnection.Encoders.SendPointRouteEncoder import SendRouteEncoder


class RouteRes(MainRes):
    # поиск пути
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("x_pos", type=float)
        parser.add_argument("y_pos", type=float)
        parser.add_argument("floor_pos", type=int)
        parser.add_argument("room_pos", type=str)
        parser.add_argument("x_place", type=float)
        parser.add_argument("y_place", type=float)
        parser.add_argument("floor_place", type=int)
        parser.add_argument("room_place", type=str)
        req = parser.parse_args()
        list_route, dist_route = self.sensCoordinator.findRoute(x_pos=req.x_pos, y_pos=req.y_pos,
                                                                floor_pos=req.floor_pos, room_pos=req.room_pos,
                                                                x_place=req.x_place, y_place=req.y_place,
                                                                floor_place=req.floor_place, room_place=req.room_place)
        sendRoute = SendRoute(distance=dist_route, route=list_route)
        dataTable = json.dumps(sendRoute, cls=SendRouteEncoder, ensure_ascii=False, sort_keys=True)
        return Response(dataTable, mimetype='application/json; charset=utf-8')
