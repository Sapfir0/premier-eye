from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from config import Config as cfg
from database.config import DatabaseConfig
import os.path
import os
# import cameraLocations
# from database.entities.cameras import DatabaseCameras

engine_parameters = {
    "convert_unicode": True,
    "pool_pre_ping": True,
    "pool_recycle": 3600,
    "echo": False,
    "connect_args": {
    'check_same_thread': False 
    }
}


class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=MetaSingleton):
    Base = None
    session = None
    engine = None

    def __init__(self):
        if (not os.path.isfile(os.path.join(cfg.APP_PATH, cfg.DATABASE_NAME))):
            print("Database not found, creating")
        else:
            print("Database founded")
        dbconfig = DatabaseConfig(cfg.APP_PATH, cfg.DATABASE_NAME)
        self.engine = create_engine(dbconfig.DATABASE_PATH, **engine_parameters)
        
        self.session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))

        self.Base = declarative_base()
        self.Base.query = self.session.query_property()
        self.Base.metadata.create_all(bind=self.engine)

        # dbcameras = DatabaseCameras()
        # cameraList = dbcameras.listCameras({})
        # index = next( (i for i,camera in enumerate(cameraList) if camera['name'] == str(cameraPath)), None) 
        # if index is None:
        #     dbcameras.post()


db = Database()
