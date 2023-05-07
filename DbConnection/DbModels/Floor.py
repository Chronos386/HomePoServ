from sqlalchemy import *
from DbConnection.DbModels.Base import Base
from DbConnection.SendModels.FloorSend import FloorSend


# Этаж
class Floor(Base):
    __tablename__ = 'floor'
    id = Column(Integer, primary_key=True)
    z_start = Column(Float)
    z_end = Column(Float)
    floor = Column(Integer)
    photo_name = Column(String(300))

    def __repr__(self):
        return f'{self.id} {self.z_start} {self.z_end} {self.floor} {self.photo_name}'

    def toSend(self) -> FloorSend:
        return FloorSend(z_start=self.z_start, z_end=self.z_end, floor=self.floor, photo_name=self.photo_name)
