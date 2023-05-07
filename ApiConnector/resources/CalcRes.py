import json
from flask import Response, request
from ApiConnector.resources.MainRes import MainRes
from DbConnection.Encoders.MyPosEncoder import MyPosEncoder
from DbConnection.SendModels.MyPosition import MyPosition


class CalcRes(MainRes):
    # поиск позиции пользователя
    def post(self):
        request_data = request.get_json()
        x, y, z = self.sensCoordinator.findCoords(
            sensor1_id=request_data['sens_dist'][0]['sens_id'],
            dist1=request_data['sens_dist'][0]['dist'],
            sensor2_id=request_data['sens_dist'][1]['sens_id'],
            dist2=request_data['sens_dist'][1]['dist'],
            sensor3_id=request_data['sens_dist'][2]['sens_id'],
            dist3=request_data['sens_dist'][2]['dist']
        )
        floor, room_name = self.sensCoordinator.calcRoomAndFloor(x=x, y=y, z=z)
        dataTable = json.dumps(MyPosition(x=x, y=y, floor=floor, room_name=room_name), cls=MyPosEncoder, ensure_ascii=False,
                               sort_keys=True)
        return Response(dataTable, mimetype='application/json')
