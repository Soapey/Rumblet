from rumblet.classes.db.SQLiteConnector import SQLiteConnector


class PlayerLockstone:
    def __init__(self, id, player_id, lockstone_name, count):
        self.id = id
        self.player_id = player_id
        self.lockstone_name = lockstone_name
        self.count = count

    def insert(self):
        with SQLiteConnector() as cur:
            query = '''
                INSERT INTO playerlockstone (player_id, lockstone_name, count)
                VALUES (?, ?, ?)
            '''
            values = (self.player_id, self.lockstone_name, self.count)
            cur.execute(query, values)
            self.id = cur.lastrowid

    def update(self):
        with SQLiteConnector() as cur:
            query = '''
                UPDATE playerlockstone
                SET player_id = ?, lockstone_name = ?, count = ?
                WHERE id = ?
            '''
            values = (self.player_id, self.lockstone_name, self.count, self.id)
            cur.execute(query, values)

    @classmethod
    def delete(cls, id):
        with SQLiteConnector() as cur:
            query = f"DELETE FROM playerlockstone WHERE id = ?"
            values = (id,)
            cur.execute(query, values)
