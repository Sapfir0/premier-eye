from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from config import Config as cfg
from database.config import DatabaseConfig

engine_parameters = {
    "convert_unicode": True,
    "pool_pre_ping": True,
    "pool_recycle": 3600,
    "echo": False,
}

dbconfig = DatabaseConfig(cfg.APP_PATH)
engine = create_engine(dbconfig.DATABASE, **engine_parameters)

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()
Base.metadata.create_all(bind=engine)


def checkConcordance():
    import os
    from database.dbAPI import getAllFilenames
    uploadedImages = []
    for address, dirs, files in os.walk(cfg.UPLOAD_FOLDER):
        for file in files:
            uploadedImages.append(file)

    imagesInDB = getAllFilenames()
    difference = list(set(uploadedImages) - set(imagesInDB)) # XOR идеален, но нет
    # думаю самое просто сказать удалите из папки с загрузками лишние изображения
    # т.к. лучше когда есть информация, но изображения нет
    # т.к. юзер не увидит изображения которых нет на диске
    if difference:
        raise Exception("Images from the database and from the folder do not match. Delete image: ", difference)


#checkConcordance()
