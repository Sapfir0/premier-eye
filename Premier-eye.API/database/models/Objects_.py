from sqlalchemy import Table, Column, Integer, String, MetaData, Enum, ForeignKey, Float, UnicodeText, literal_column, DateTime, Boolean, or_
from database import db
from datetime import datetime


class Objects_(db.Base):
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    scores = Column(Float)

    type = Column(String(20))
    imageId = Column(Integer)
    coordinatesId = Column(Integer)
    createdAt = Column(DateTime, default=datetime.now())
    updatedAt = Column(DateTime, default=datetime.now())

    def __init__(self, scores=scores, type=type, imageId=imageId, coordinatesId=coordinatesId):
        self.scores = scores
        self.type = type
        self.imageId = imageId
        self.coordinatesId = coordinatesId
