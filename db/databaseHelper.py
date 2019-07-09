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
    fixationDatetime = Column( DateTime ) # unque добавить
    LUx = Column(Integer) # Left Up
    LUy= Column(Integer)
    RDx= Column(Integer) # Right Down
    RDy= Column(Integer)
    CDx= Column(Integer) # Center Down центр нижней стороны
    CDy= Column(Integer)
    #Column('GPS', Integer,),
    #Column('objectId', Integer,)

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def init_db():
        Base.metadata.create_all(bind=engine)
        #metadata.create_all(engine)
        db_session.commit()

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)