from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Float, DateTime, Boolean, or_, DATETIME, TIMESTAMP
from database import db
from datetime import datetime


class Images(db.Base):
    __tablename__ = "images"

    def init_db(self):
        db.Base.metadata.create_all(bind=engine)
        db.session.commit()

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    path = Column(String(250), unique=True)
    filename = Column(String(30), unique=True)
    numberOfCam = Column(Integer)
    fixationDatetime = Column(DateTime, unique=True)
    createdAt = Column(DateTime, default=datetime.now())
    updatedAt = Column(DateTime, default=datetime.now())

    def __init__(self, imagePath: str, filename: str, numberOfCam: int, fixationDatetime):
        self.init_db()
        self.path = imagePath
        self.filename = filename
        self.numberOfCam = numberOfCam
        self.fixationDatetime = fixationDatetime

