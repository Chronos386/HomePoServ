from sqlalchemy import *
from DbConnection.DbModels.Base import Base


# Общие размеры территории
class Territory(Base):
    __tablename__ = 'territory'
    id = Column(Integer, primary_key=True)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)

    def __repr__(self):
        return f'{self.id} {self.x} {self.y} {self.z}'
