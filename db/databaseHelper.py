from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Float, UnicodeText, literal_column, DateTime, Boolean, or_
from sqlalchemy.orm import scoped_session, sessionmaker, aliased
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy import func
import settings as cfg


engine = create_engine(cfg.DATABASE,  convert_unicode=True, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


dbName = 'object.sqlite'



metadata.create_all(engine)

class Objects(object):
    __tablename__ =  "objects"

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def init_db():
        metadata = MetaData() 
        table = Table(__tablename__, metadata,
            Column('id', Integer, primary_key=True),
            Column('LUx', Integer),
            Column('LUy', Integer),
            Column('RDx', Integer),
            Column('RDy', Integer),
            Column('CDx', Integer),
            Column('CDy', Integer),
            Column('GPS', Integer,),
            Column('objectId', Integer,)
        )



    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)