from sqlalchemy import *
from DbConnection.DbModels.Base import Base


# Место на карте
class Place(Base):
    __tablename__ = 'place'
    id = Column(Integer, primary_key=True)
    x = Column(Float)
    y = Column(Float)
    is_class = Column(BOOLEAN)
    room = Column(String(150))
    floor_id = Column(Integer, ForeignKey('floor.id'))
    name = Column(String(150))
    description = Column(String(600))
    photo_name = Column(String(300))

    def __repr__(self):
        return f'{self.id} {self.x} {self.y} {self.is_class} {self.room} {self.floor_id} {self.name} {self.description} ' \
               f'{self.photo_name}'
