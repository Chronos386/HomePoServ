from DbConnection.DbModels.Floor import Floor
from DbConnection.DbModels.Place import Place
from DbConnection.DbModels.Territory import Territory
from DbConnection.DbModels.SensorBLE import SensorBLE


class Getter:
    def __init__(self, session):
        self.session = session

    def getCountSensor(self):
        return self.session.query(SensorBLE).count()

    def getAllSensors(self):
        allSensors = self.session.query(SensorBLE).all()
        return allSensors

    def getSensorById(self, sensor_id):
        sensorDB = self.session.query(SensorBLE).filter_by(id=sensor_id).first()
        return sensorDB

    def getTerritory(self):
        sensorDB = self.session.query(Territory).filter_by(id=1).first()
        return sensorDB

    def getCountFloors(self):
        return self.session.query(Floor).count()

    def getAllFloors(self):
        allFloors = self.session.query(Floor).all()
        return allFloors

    def getFloorByFloor(self, floor):
        floorDB = self.session.query(Floor).filter_by(floor=floor).first()
        return floorDB

    def getFloorById(self, floor_id):
        floorDB = self.session.query(Floor).filter_by(id=floor_id).first()
        return floorDB

    def getCountPlaces(self):
        return self.session.query(Place).count()

    def getAllPlaces(self):
        allPlaces = self.session.query(Place).all()
        return allPlaces

    def getPlaceById(self, place_id):
        placeDB = self.session.query(Place).filter_by(id=place_id).first()
        return placeDB
