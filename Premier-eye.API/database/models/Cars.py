from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base
from datetime import datetime


class Cars(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    carNumber = Column(String(15))
    objectId = Column(Integer)
    createdAt = Column(DateTime, default=datetime.now())
    updatedAt = Column(DateTime, default=datetime.now())

    def __init__(self, carNumber=carNumber, objectId=objectId):
        self.carNumber = carNumber
        self.objectId = objectId

