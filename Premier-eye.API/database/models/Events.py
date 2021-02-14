from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import db
from datetime import datetime


class Events(db.Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    timestamp = Column(String)
    title = Column(String)
    cameraId = Column(Integer, default=None)

    def __init__(self, timestamp, title, cameraId):
        self.timestamp = timestamp
        self.title = title
        self.cameraId = cameraId




