from DbConnection.DbModels.Floor import Floor
from DbConnection.DbModels.Place import Place
from DbConnection.DbModels.Territory import Territory
from DbConnection.DbModels.SensorBLE import SensorBLE


class Setter:
    def __init__(self, session):
        self.session = session

    def __findFirstFreeID(self, table_db):
        stmt = self.session.query(table_db).order_by(table_db.id.asc()).all()
        count = self.session.query(table_db).count()
        mass = []
        for i in range(1, count + 1):
            if i != stmt[i - 1].id:
                mass.append(i)
        if len(mass) != 0:
            count = mass[0]
        else:
            count += 1
        return count

    def setTerritory(self, x: float, y: float, z: float):
        self.session.query(Territory).filter_by(id=1).delete(synchronize_session=False)
        self.session.commit()
        new_id = self.__findFirstFreeID(Territory)
        new_terr = Territory(id=new_id, x=x, y=y, z=z)
        self.session.add(new_terr)
        self.session.commit()

    def addSensor(self, x: float, y: float, z: float) -> int:
        new_id = self.__findFirstFreeID(SensorBLE)
        new_sensor = SensorBLE(id=new_id, x=x, y=y, z=z)
        self.session.add(new_sensor)
        self.session.commit()
        return new_id

    def updSensor(self, sensor_id: int, x: float, y: float, z: float):
        sensor = self.session.query(SensorBLE).filter_by(id=sensor_id).first()
        sensor.x = x
        sensor.y = y
        sensor.z = z
        self.session.commit()

    def delSensor(self, sensor_id: int):
        self.session.query(SensorBLE).filter_by(id=sensor_id).delete(synchronize_session=False)
        self.session.commit()

    def addFloor(self, z_start: float, z_end: float, floor: int, photo: str):
        new_id = self.__findFirstFreeID(Floor)
        new_floor = Floor(id=new_id, z_start=z_start, z_end=z_end, floor=floor, photo_name=photo)
        self.session.add(new_floor)
        self.session.commit()
        return new_id

    def updFloor(self, z_start: float, z_end: float, floor: int, photo: str):
        place = self.session.query(Floor).filter_by(floor=floor).first()
        place.z_start = z_start
        place.z_end = z_end
        place.floor = floor
        if photo != "":
            place.photo_name = photo
        self.session.commit()

    def updFloorPhoto(self, floor: int, photo: str):
        place = self.session.query(Floor).filter_by(floor=floor).first()
        place.photo_name = photo
        self.session.commit()

    def delFloor(self, floor: int):
        self.session.query(Floor).filter_by(floor=floor).delete(synchronize_session=False)
        self.session.commit()

    def addPlace(self, x: float, y: float, room: str, floor_id: int, name: str, descr: str, photo: str,
                 is_class: bool) -> int:
        new_id = self.__findFirstFreeID(Place)
        new_place = Place(id=new_id, x=x, y=y, is_class=is_class, room=room, floor_id=floor_id, name=name,
                          description=descr, photo_name=photo)
        self.session.add(new_place)
        self.session.commit()
        return new_id

    def updPlace(self, place_id: int, x: float, y: float, room: str, floor_id: int, name: str, descr: str, photo: str,
                 is_class: bool):
        place = self.session.query(Place).filter_by(id=place_id).first()
        place.x = x
        place.y = y
        place.room = room
        place.floor_id = floor_id
        place.name = name
        place.description = descr
        place.is_class = is_class
        if photo != "":
            place.photo_name = photo
        self.session.commit()

    def delPlace(self, place_id: int):
        self.session.query(Place).filter_by(id=place_id).delete(synchronize_session=False)
        self.session.commit()
