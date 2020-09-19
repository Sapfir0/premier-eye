from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base
from datetime import datetime


class Coordinates(Base):
    __tablename__ = "coordinates"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    LDx = Column(Integer)  # Left Down
    LDy = Column(Integer)
    RUx = Column(Integer)  # Right Up
    RUy = Column(Integer)
    createdAt = Column(DateTime, default=datetime.now())
    updatedAt = Column(DateTime, default=datetime.now())

    def __init__(self, coord):
        self.LDx = coord[0]
        self.LDy = coord[1]
        self.RUx = coord[2]
        self.RUy = coord[3]




