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
    
    def rowCount(self, table):
        return db.session.query(table).count()

    def get(self, table, id):
        return self.getWhere(table, (table.id == id))

    def getWhere(self, table, whereStmt, multiple=False):
        selectStmt = select([table]).where(whereStmt)
        query = self.conn.execute(selectStmt)
        if not multiple:
            row = query.fetchone()
            return row if row == None else dict(row)
        else:
            return [dict(i) for i in query.fetchall()]

    def post(self, table, **entityFields):
        insertStmt = insert(table).values(**entityFields)
        res = self.conn.execute(insertStmt)
        return res