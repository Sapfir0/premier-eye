from enum import Enum
import os


class databasesDialect(Enum):
    sqlite = "sqlite"
    mysql = "mysql"


class DatabaseConfig:
    DATABASE_PATH = ''
    APP_PATH = ''

    def __init__(self, APP_PATH, DATABASE_NAME):
        self.APP_PATH = APP_PATH
        self.DATABASE_PATH = self.getDatabasePath(databasesDialect.sqlite, DATABASE_NAME)

    def getDatabasePath(self, dialect: databasesDialect, dbName):
        if dialect.sqlite == dialect:
            database = "sqlite:///" + os.path.join(self.APP_PATH, dbName)
        elif dialect.mysql == dialect:
            username = os.environ.get("DB_USERNAME")
            password = os.environ.get("DB_PASSWORD")
            host = os.environ.get("DB_HOST")
            databaseName = os.environ.get("DB_NAME")
            database = f"mysql+mysqldb://{username}:{password}@{host}/{databaseName}"
        else:
            raise Exception("Undefined database")
        return database
