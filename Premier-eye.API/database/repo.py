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
        return self.getWhere(table, (table.id == id))

    def getWhere(self, table, whereStmt, multiple=False):
        selectStmt = select([table]).where(whereStmt)
        res = self.conn.execute(selectStmt)
        if not multiple:
            return dict(res.fetchone())
        else:
            return [dict(i) for i in res.fetchall()]

    def post(self, table, **entityFields):
        insertStmt = insert(table).values(**entityFields)
        res = self.conn.execute(insertStmt)
        return res