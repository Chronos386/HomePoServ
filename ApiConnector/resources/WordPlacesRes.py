from flask import Response
from flask_restful import reqparse
from ApiConnector.resources.MainRes import MainRes


class WordPlacesRes(MainRes):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("only_class", type=bool)
        parser.add_argument("search_by_floor", type=bool)
        parser.add_argument("floor", type=int)
        req = parser.parse_args()
        places = self.dbClass.getPlaceByFiltersJSON(
            substring=req.name,
            only_class=req.only_class,
            search_by_floor=req.search_by_floor,
            need_floor=req.floor
        )
        return Response(places, mimetype='application/json; charset=utf-8')
