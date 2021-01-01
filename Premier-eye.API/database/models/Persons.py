from sqlalchemy import Column, Integer, DateTime
from database import db
from datetime import datetime


class Persons(db.Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    objectId = Column(Integer)
    createdAt = Column(DateTime, default=datetime.now())
    updatedAt = Column(DateTime, default=datetime.now())

    def __init__(self, objectId=objectId):
        self.objectId = objectId
