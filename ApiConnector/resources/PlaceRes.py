from flask import Response
from ApiConnector.resources.MainRes import MainRes


class PlaceRes(MainRes):
    def get(self, place_id):
        place = self.dbClass.getPlaceByIdJSON(place_id=place_id)
        return Response(place, mimetype='application/json; charset=utf-8')
