from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import db
from datetime import datetime


class Camera(db.Base):
    __tablename__ = "camera"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(35))
    location = Column(String(15), nullable=True)
    createdAt = Column(DateTime, default=datetime.now())
    updatedAt = Column(DateTime, default=datetime.now())

    def __init__(self, name=name, location=location):
        self.location = location
        self.name = name


