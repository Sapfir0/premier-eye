from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Float, UnicodeText, literal_column, DateTime, Boolean, or_
from sqlalchemy.orm import scoped_session, sessionmaker, aliased
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy import func
import settings as cfg
import sqlalchemy as sql

engine = create_engine(cfg.DATABASE,  convert_unicode=True, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base() 
Base.query = db_session.query_property()


class Objects(Base):
    __tablename__ =  "objects" 

    id = Column(Integer, primary_key=True)
    numberOfCam = Column(Integer)
    fixationDatetime = Column( DateTime ) # unque добавить
    LUx = Column(Integer) # Left Up
    LUy= Column(Integer)
    RDx= Column(Integer) # Right Down
    RDy= Column(Integer)
    CDx= Column(Integer) # Center Down центр нижней стороны
    CDy= Column(Integer)
    #Column('GPS', Integer,),
    #Column('objectId', Integer,)

    def __init__(self, numberOfCam, fixationDatetime, LUx, LUy, RDx, RDy, CDx, CDy):
        self.numberOfCam = numberOfCam
        self.fixationDatetime, 
        self.LUx = LUx
        self.LUy = LUy
        self.RDx = RDx
        self.RDy = RDy
        self.CDx = CDx
        self.CDy = CDy


    def init_db():
        Base.metadata.create_all(bind=engine)
        db_session.commit()

    def __repr__(self):
        return "<Object('%d','%s', '[%d', '%d]','[%d', '%d]','[%d', '%d]')>" % (self.numberOfCam, self.fixationDatetime, self.LUx, self.LUy, self.RDx, self.RDy, self.CDx, self.CDy)
