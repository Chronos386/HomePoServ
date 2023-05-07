import json
from sqlalchemy import *
from Models.DistCord import DistCord
from sqlalchemy.orm import sessionmaker
from DbConnection.GetSet.Getter import Getter
from DbConnection.GetSet.Setter import Setter
from DbConnection.SendModels.PlaceSend import PlaceSend
from DbConnection.Encoders.PlaceEncoder import PlaceEncoder
from DbConnection.Encoders.FloorEncoder import FloorEncoder
from DbConnection.Encoders.SensorEncoder import SensorEncoder
from DbConnection.SendModels.TerritorySend import TerritorySend
from DbConnection.Encoders.TerritorySendEncoder import TerritorySendEncoder


class DBClass:
    def __init__(self):
        self.engine = create_engine("postgresql+psycopg2://postgres:Chronos386@localhost/home_pos_db")
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.getter = Getter(self.session)
        self.setter = Setter(self.session)

    def getTerritoryInf(self):
        terr = self.getter.getTerritory()
        return terr.x, terr.y, terr.z

    def getTerritoryJSON(self):
        territory = self.getter.getTerritory()
        dataTable = json.dumps(TerritorySend(x=territory.x, y=territory.y, z=territory.z), cls=TerritorySendEncoder,
                               ensure_ascii=False, sort_keys=True)
        return dataTable

    def updTerritory(self, x: float, y: float, z: float):
        self.setter.setTerritory(x=x, y=y, z=z)

    def setTerritoryInform(self, x, y, z):
        self.setter.setTerritory(x=x, y=y, z=z)

    def findSensorForCalc(self, sensor_id, dist) -> DistCord:
        sensor = self.getter.getSensorById(sensor_id=sensor_id)
        return DistCord(x=sensor.x, y=sensor.y, z=sensor.z, dist=dist)

    def getSensorJSON(self, sensor_id):
        sensor = self.getter.getSensorById(sensor_id=sensor_id)
        dataTable = json.dumps(sensor.toSend(), cls=SensorEncoder, ensure_ascii=False, sort_keys=True)
        return dataTable

    def getAllSensorsJSON(self):
        sensors = self.getter.getAllSensors()
        sendSensors = []
        for sens in sensors:
            sendSensors.append(sens.toSend())
        dataTable = json.dumps(sendSensors, cls=SensorEncoder, ensure_ascii=False, sort_keys=True)
        return dataTable

    def addNewSensor(self, x: float, y: float, z: float):
        self.setter.addSensor(x=x, y=y, z=z)

    def updSensor(self, sensor_id: int, x: float, y: float, z: float):
        self.setter.updSensor(sensor_id=sensor_id, x=x, y=y, z=z)

    def delSensor(self, sensor_id: int):
        self.setter.delSensor(sensor_id=sensor_id)

    def getAllFloorsJSON(self):
        floors = self.getter.getAllFloors()
        sendFloors = []
        for floor in floors:
            sendFloors.append(floor.toSend())
        dataTable = json.dumps(sendFloors, cls=FloorEncoder, ensure_ascii=False, sort_keys=True)
        return dataTable

    def findFloorsByZ(self, z: float):
        floors = self.getter.getAllFloors()
        for floor in floors:
            if (z >= floor.z_start) & (z <= floor.z_end):
                return floor.floor

    def getFloorJSON(self, floor):
        floor = self.getter.getFloorByFloor(floor=floor)
        dataTable = json.dumps(floor.toSend(), cls=FloorEncoder, ensure_ascii=False, sort_keys=True)
        return dataTable

    def getFloorPhoto(self, floor) -> str:
        floor = self.getter.getFloorByFloor(floor=floor)
        return floor.photo_name

    def addNewFloor(self, z_start: float, z_end: float, floor: int, photo: str):
        self.setter.addFloor(z_start=z_start, z_end=z_end, floor=floor, photo=photo)

    def updFloor(self, z_start: float, z_end: float, floor: int, photo: str):
        self.setter.updFloor(z_start=z_start, z_end=z_end, floor=floor, photo=photo)

    def updFloorPhoto(self, floor: int, photo: str):
        self.setter.updFloorPhoto(floor=floor, photo=photo)

    def delFloor(self, floor):
        self.setter.delFloor(floor=floor)

    def getAllPlacesJSON(self):
        places = self.getter.getAllPlaces()
        sub_places = []
        for place in places:
            floor = self.getter.getFloorById(floor_id=place.floor_id)
            sub_places.append(PlaceSend(place_id=place.id, x=place.x, y=place.y, is_class=place.is_class,
                                        floor=floor.floor, room_name=place.room, name=place.name,
                                        description=place.description, photo_name=place.photo_name))
        dataTable = json.dumps(sub_places, cls=PlaceEncoder, ensure_ascii=False, sort_keys=True)
        return dataTable

    def getPlaceByWordJSON(self, substring: str):
        places = self.getter.getAllPlaces()
        sub_places = []
        for place in places:
            if substring in place.name:
                floor = self.getter.getFloorById(floor_id=place.floor_id)
                sub_places.append(PlaceSend(place_id=place.id, x=place.x, y=place.y, is_class=place.is_class,
                                            floor=floor.floor, room_name=place.room, name=place.name,
                                            description=place.description, photo_name=place.photo_name))
        dataTable = json.dumps(sub_places, cls=PlaceEncoder, ensure_ascii=False, sort_keys=True)
        return dataTable

    def getPlaceByFiltersJSON(self, substring: str, only_class: bool, search_by_floor: bool, need_floor: int):
        places = self.getter.getAllPlaces()
        sub_places = []
        for place in places:
            if substring.lower() in place.name.lower():  # /////////////////////////////////////////////////////////////
                floor = self.getter.getFloorById(floor_id=place.floor_id)
                if (search_by_floor & (floor.floor == need_floor)) | (search_by_floor is False):  # ////////////////////
                    if (only_class & place.is_class) | (only_class is False):  # ///////////////////////////////////////
                        sub_places.append(PlaceSend(place_id=place.id, x=place.x, y=place.y, is_class=place.is_class,
                                                    floor=floor.floor, room_name=place.room, name=place.name,
                                                    description=place.description, photo_name=place.photo_name))
        dataTable = json.dumps(sub_places, cls=PlaceEncoder, ensure_ascii=False, sort_keys=True)
        return dataTable

    def getPlaceByIdJSON(self, place_id: int):
        place = self.getter.getPlaceById(place_id=place_id)
        floor = self.getter.getFloorById(floor_id=place.floor_id)
        placeSend = PlaceSend(place_id=place.id, x=place.x, y=place.y, is_class=place.is_class, floor=floor.floor,
                              room_name=place.room, name=place.name, description=place.description,
                              photo_name=place.photo_name)
        dataTable = json.dumps(placeSend, cls=PlaceEncoder, ensure_ascii=False, sort_keys=True)
        return dataTable

    def addNewPlace(self, x: float, y: float, room: str, floor: int, name: str, descr: str, photo: str, is_class: bool):
        floor_id = self.getter.getFloorByFloor(floor=floor)
        self.setter.addPlace(x=x, y=y, room=room, floor_id=floor_id.id, name=name, descr=descr, photo=photo,
                             is_class=is_class)

    def updPlace(self, place_id: int, x: float, y: float, room: str, floor: int, name: str, descr: str, photo: str,
                 is_class: bool):
        floor_id = self.getter.getFloorByFloor(floor=floor)
        self.setter.updPlace(place_id=place_id, x=x, y=y, room=room, floor_id=floor_id.id, name=name, descr=descr,
                             photo=photo, is_class=is_class)

    def delPlace(self, place_id: int):
        self.setter.delPlace(place_id=place_id)
