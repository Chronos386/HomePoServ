import os
import json
from math import fabs
from scipy.optimize import fsolve
from Models.DistCord import DistCord
from DbConnection.DbClass import DBClass
from Models.SendPointRoute import SendPointRoute
from CalcClasses.RouteCalculator import RouteCalculator
from DbConnection.SendModels.SensorSend import SensorSend


def sortByZ(mass_ans):
    for i in range(3):
        for j in range(3):
            if j != i:
                if mass_ans[i].z < mass_ans[j].z:
                    temp = mass_ans[j]
                    mass_ans[j] = mass_ans[i]
                    mass_ans[i] = temp


def pointInPolygon(x, y, xp, yp):
    c = 0
    for i in range(len(xp)):
        if (((yp[i] <= y < yp[i - 1]) or (yp[i - 1] <= y < yp[i])) and
                (x > (xp[i - 1] - xp[i]) * (y - yp[i]) / (yp[i - 1] - yp[i]) + xp[i])):
            c = 1 - c
    return c


def pointsDistance(x1, y1, x2, y2) -> float:
    return (((x1 - x2) ** 2) + ((y1 - y2) ** 2)) ** 0.5


class SensorCoordinator:
    a: DistCord = None
    b: DistCord = None
    c: DistCord = None

    def __init__(self):
        self.dbClass = DBClass()
        self.routeCalc = RouteCalculator()
        self.rout_files = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Files')

    def __tryCalcCoord(self, p):
        x4, y4, z4 = p
        x1, y1, z1 = self.a.coord
        x2, y2, z2 = self.b.coord
        x3, y3, z3 = self.c.coord
        return (
            ((x4 - x1) ** 2) + ((y4 - y1) ** 2) + ((z4 - z1) ** 2) - (self.a.dist ** 2),
            ((x4 - x2) ** 2) + ((y4 - y2) ** 2) + ((z4 - z2) ** 2) - (self.b.dist ** 2),
            ((x4 - x3) ** 2) + ((y4 - y3) ** 2) + ((z4 - z3) ** 2) - (self.c.dist ** 2)
        )

    def findCoords(self, sensor1_id: int, dist1: float, sensor2_id: int, dist2: float, sensor3_id: int, dist3: float):
        self.a = self.dbClass.findSensorForCalc(sensor_id=sensor1_id, dist=dist1)
        self.b = self.dbClass.findSensorForCalc(sensor_id=sensor2_id, dist=dist2)
        self.c = self.dbClass.findSensorForCalc(sensor_id=sensor3_id, dist=dist3)
        mass = [self.a, self.b, self.c]
        mass_ans = []
        x, y, z = (-1, -1, -1)
        count = 0
        while count != 3:
            x, y, z = mass[count].coord
            x, y, z = fsolve(self.__tryCalcCoord, (x, y, z), xtol=10 ** -10)
            mass_ans.append(SensorSend(sensor_id=0, x=x, y=y, z=z))
            count += 1
        if (mass_ans[0].z > 10) & (mass_ans[1].z > 10) & (mass_ans[2].z > 10):
            checker_equals = []
            sortByZ(mass_ans)
            for i in range(2):
                for j in range(i + 1, 3):
                    if (fabs(mass_ans[i].x - mass_ans[j].x) < 10) & (fabs(mass_ans[i].y - mass_ans[j].y) < 10):
                        checker_equals.append(True)
                    else:
                        checker_equals.append(False)
            count = 0
            while count != 3:
                if checker_equals[count]:
                    return mass_ans[1].x, mass_ans[1].y, mass_ans[1].z
                count += 1
        else:
            x, y, z = (1, 1, 1)
            x, y, z = fsolve(self.__tryCalcCoord, (x, y, z), xtol=10 ** -10)
            if z > 10:
                return x, y, z
            sortByZ(mass_ans)
            house_x, house_y, house_z = self.dbClass.getTerritoryInf()
            value_11 = mass_ans[0].x / (house_x / 100.0)
            value_12 = mass_ans[0].y / (house_y / 100.0)
            value_21 = mass_ans[1].x / (house_x / 100.0)
            value_22 = mass_ans[1].y / (house_y / 100.0)
            if (((value_11 > 40) & (value_11 < 65)) & ((value_12 > 30) & (value_12 < 65))) | \
                    (((value_21 > 40) & (value_21 < 65)) & ((value_22 > 30) & (value_22 < 65))):
                return mass_ans[0].x, mass_ans[0].y, mass_ans[2].z
            else:
                return mass_ans[2].x, mass_ans[2].y, mass_ans[2].z
        return x, y, z

    def calcRoom(self, x: float, y: float, floor: int) -> str:
        room_name = ""
        with open(self.rout_files + '/roomPoints.json', encoding="utf-8") as json_file:
            rooms = json.load(json_file)
            for room in rooms:
                if room['floor'] == floor:
                    xp = []
                    yp = []
                    for point in room['points']:
                        xp.append(point['x'])
                        yp.append(point['y'])
                    if pointInPolygon(x=x, y=y, xp=xp, yp=yp) == 1:
                        room_name = room['name']
        return room_name

    def calcRoomAndFloor(self, x: float, y: float, z: float) -> (int, str):
        floor = self.dbClass.findFloorsByZ(z=z)
        room_name = self.calcRoom(x=x, y=y, floor=floor)
        return floor, room_name

    def __findNearPoint(self, x: float, y: float, floor: int, room: str) -> int:
        myIndex: int = -1
        distance: float = 1000000000
        with open(self.rout_files + '/homePositionPoints.json', encoding="utf-8") as json_file:
            points = json.load(json_file)
            for point in points:
                if (point['floor'] == floor) & (point['room'] == room):
                    if pointsDistance(point['x'], point['y'], x, y) < distance:
                        myIndex = point['id'] - 1
                        distance = pointsDistance(point['x'], point['y'], x, y)
        return myIndex

    def findRoute(self, x_pos: float, y_pos: float, floor_pos: int, room_pos: str, x_place: float, y_place: float,
                  floor_place: int, room_place: str) -> tuple:
        startPoint = self.__findNearPoint(x_pos, y_pos, floor_pos, room_pos)
        endPoint = self.__findNearPoint(x_place, y_place, floor_place, room_place)
        route, find_dist = self.routeCalc.runAndFind(start=startPoint, end=endPoint)
        routePoints = [SendPointRoute(x_pos, y_pos, floor_pos, room_pos)]
        with open(self.rout_files + '/homePositionPoints.json', encoding="utf-8") as json_file:
            points = json.load(json_file)
            for routePoint in route:
                for point in points:
                    if (point['id'] - 1) == routePoint:
                        routePoints.append(SendPointRoute(point['x'], point['y'], point['floor'], point['room']))
        routePoints.append(SendPointRoute(x_place, y_place, floor_place, room_place))
        return routePoints, find_dist
