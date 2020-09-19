from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Float, DateTime, Boolean, or_, DATETIME, TIMESTAMP
from database import Base
from database import session
from database import engine
from datetime import datetime


class Images(Base):
    __tablename__ = "images"

    def init_db(self):
        Base.metadata.create_all(bind=engine)
        session.commit()

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    path = Column(String(250), unique=True)
    filename = Column(String(30), unique=True)
    numberOfCam = Column(Integer)
    fixationDatetime = Column(DateTime, unique=True)
    hasObjects = Column(Boolean)
    createdAt = Column(DateTime, default=datetime.now())
    updatedAt = Column(DateTime, default=datetime.now())

    def __init__(self, imagePath: str, filename: str, numberOfCam: int, fixationDatetime, hasObjects: bool):
        self.init_db()
        self.path = imagePath
        self.filename = filename
        self.numberOfCam = numberOfCam
        self.fixationDatetime = fixationDatetime
        self.hasObjects = hasObjects

