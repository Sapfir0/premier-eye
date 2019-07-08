from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Float, UnicodeText, literal_column, DateTime, Boolean, or_
from sqlalchemy import create_engine
import settings as cfg

engine = create_engine(cfg.DATABASE,  convert_unicode=True, echo=True)
db_session


__tablename__ =  "params"
dbName = 'object.sqlite'


metadata = MetaData() 
table = Table(tablename, metadata,
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

metadata.create_all()