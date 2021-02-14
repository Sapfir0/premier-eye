from database import db
from sqlalchemy import select, insert

class Repo:
    conn = None

    def __init__(self):
        self.conn = db.engine.connect()

    def all(self, table):
        selectStmt = select([table])
        res = self.conn.execute(selectStmt).fetchall()
        stringRes = [dict(i) for i in res]
        return stringRes
    
    def get(self, table, id):
        selectStmt = select([table]).where(table.id == id)
        res = self.conn.execute(selectStmt).fetchone()
        return res

    def post(self, table, **entityFields):
        insertStmt = insert(table).values(**entityFields)
        res = self.conn.execute(insertStmt)
        return res