from sqlalchemy import *
from DbConnection.DbModels.Base import Base


# Категория места
class Place(Base):
    __tablename__ = 'placecategories'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))

    def __repr__(self):
        return f'{self.id} {self.name}'
