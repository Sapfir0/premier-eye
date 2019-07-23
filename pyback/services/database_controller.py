from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Float, UnicodeText, literal_column, DateTime, Boolean, or_
from sqlalchemy.orm import scoped_session, sessionmaker, aliased
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy import func
from settings import Settings as cfg
import sqlalchemy as sql

engine = create_engine(cfg.DATABASE, convert_unicode=True, echo=False)
session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine))  # хм сложная строчка

Base = declarative_base()
Base.query = session.query_property()


class Objects(Base):
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True, unique=True)
    numberOfCam = Column(Integer)
    fixationDatetime = Column(DateTime)  # unque добавить
    LDx = Column(Integer)  # Left Down
    LDy = Column(Integer)
    RUx = Column(Integer)  # Right Up
    RUy = Column(Integer)
    CDx = Column(Integer)  # Center Down 
    CDy = Column(Integer)
    carNumber = Column(String)
    #Column('objectId', Integer,)
    #Column('GPS', Integer,),

    def __init__(
            self,
            numberOfCam,
            fixationDatetime,
            LDx, LDy,
            RUx, RUy,
            CDx, CDy,
            carNumber):
        self.numberOfCam = numberOfCam
        self.fixationDatetime = fixationDatetime
        self.LDx = LDx
        self.LDy = LDy
        self.RUx = RUx
        self.RUy = RUy
        self.CDx = CDx
        self.CDy = CDy
        self.carNumber = carNumber

    def init_db():
        Base.metadata.create_all(bind=engine)
        session.commit()

    def __repr__(self):
        return "<Object('%s','%s', '[%d', '%d]','[%d', '%d]','[%d', '%d]')>" % (
            self.numberOfCam, self.fixationDatetime, self.LDx, self.LDy, self.RUx, self.RUy, self.CDx, self.CDy, self.curNumber)

    def checkQuery(self):
        for i in session.query(Objects):
            print(i)

def writeInfoForObjectInDB(numberOfCam, fixationDatetime, rectCoordinates, centerDown, carNumber):
    LUy, LUx, RDy, RDx = rectCoordinates
    CDx, CDy = centerDown
    objN = Objects(numberOfCam, fixationDatetime, int(LUx), int(LUy), int(RDx), int(RDy), int(CDx), int(CDy), carNumber)
    session.add(objN)
    session.commit()
    session.flush() # можно один раз добавить  


import settings
cfg = settings.Settings()

Objects.init_db()
