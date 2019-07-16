from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Float, UnicodeText, literal_column, DateTime, Boolean, or_
from sqlalchemy.orm import scoped_session, sessionmaker, aliased
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy import func
from settings import Settings as cfg
import sqlalchemy as sql

print(cfg.DATABASE)
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
    CDx = Column(Integer)  # Center Down центр нижней стороны
    CDy = Column(Integer)
    #Column('GPS', Integer,),
    #Column('objectId', Integer,)

    def __init__(
            self,
            numberOfCam,
            fixationDatetime,
            LDx,
            LDy,
            RUx,
            RUy,
            CDx,
            CDy):
        self.numberOfCam = numberOfCam
        self.fixationDatetime = fixationDatetime
        self.LDx = LDx
        self.LDy = LDy
        self.RUx = RUx
        self.RUy = RUy
        self.CDx = CDx
        self.CDy = CDy

    def init_db():
        Base.metadata.create_all(bind=engine)
        session.commit()

    def __repr__(self):
        return "<Object('%s','%s', '[%d', '%d]','[%d', '%d]','[%d', '%d]')>" % (
            self.numberOfCam, self.fixationDatetime, self.LDx, self.LDy, self.RUx, self.RUy, self.CDx, self.CDy)

        # object = {
        #     "numberOfCam": self.numberOfCam,
        #     "fixationDatetime": self.fixationDatetime,
        #     "LDx": self.LDx,
        #     "LDy": self.LDy,
        #     "RUx": self.RUx,
        #     "RUy": self.RUy,
        #     "CDx": self.CDx,
        #     "CDy": self.CDy
        # }
        # return object

    def checkQuery():
        for i in session.query(Objects):
            print(i)


Objects.init_db()
