from flask_restful import Resource
from DbConnection.DbClass import DBClass
from CalcClasses.SensorCoordinator import SensorCoordinator


class MainRes(Resource):
    def __init__(self):
        self.dbClass = DBClass()
        self.sensCoordinator = SensorCoordinator()
