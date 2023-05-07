from sqlalchemy import *
from DbConnection.DbModels.Base import Base
from DbConnection.SendModels.SensorSend import SensorSend


# BLE датчики
class SensorBLE(Base):
    __tablename__ = 'sensorble'
    id = Column(Integer, primary_key=True)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)

    def __repr__(self):
        return f'{self.id} {self.x} {self.y} {self.z}'

    def toSend(self) -> SensorSend:
        return SensorSend(sensor_id=self.id, x=self.x, y=self.y, z=self.z)
