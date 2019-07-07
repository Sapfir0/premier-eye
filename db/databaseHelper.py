import sqlite3

tableName =  "params"
dbName = 'object.sqlite'

conn = sqlite3.connect(dbName)

cursor = conn.cursor()


cursor.execute(f"""CREATE TABLE IF NOT EXISTS {tableName}  (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    numberOfCam INTEGER NOT NULL,
    fixationTime BLOB NOT NULL,
    LUx INTEGER NOT NULL,
    LUy INTEGER NOT NULL,
    RDx INTEGER NOT NULL,
    RDy INTEGER NOT NULL,
    objectId INTEGER NOT NULL,
    GPScoordinates INTEGER  ); """)

conn.commit()

conn.close()

def writeInDB(numberOfCam, fixationTime, LUx, LUy, RDx, RDy, objectId=0, GPScoordinates=None):
    cursor.execute(f"""insert into {tableName}  (
    {numberOfCam} ,
    {fixationTime},
    {leftUpCoordinates},
    {rightDownCoordinates},
    {objectId},
    {GPScoordinates}  ); """)
    conn.commit()

def readFromDB():
    cursor.execute(f"SELECT * FROM {tableName};")


