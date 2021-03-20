from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import db
from datetime import datetime


class Coordinates(db.Base):
    __tablename__ = "coordinates"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    LUx = Column(Integer) 
    LUy = Column(Integer)
    RDx = Column(Integer)  
    RDy = Column(Integer)
    createdAt = Column(DateTime, default=datetime.now())
    updatedAt = Column(DateTime, default=datetime.now())

    def __init__(self, coord):
        self.LUy, self.LUx, self.RDy, self.RDx = coord





