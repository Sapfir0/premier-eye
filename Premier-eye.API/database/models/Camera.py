from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base
from datetime import datetime


class Camera(Base):
    __tablename__ = "camera"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    location = Column(String(15))
    createdAt = Column(DateTime, default=datetime.now())
    updatedAt = Column(DateTime, default=datetime.now())

    def __init__(self, location=location):
        self.location = location


