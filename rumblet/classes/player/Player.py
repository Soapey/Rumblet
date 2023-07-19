from rumblet.classes.db.SQLiteConnector import SQLiteConnector
from rumblet.classes.player.PlayerLockstone import PlayerLockstone
from rumblet.classes.LockstoneList import LockstoneList

class Player:
    def __init__(self, id, name, money):
        self.id = id
        self.name = name
        self.money = money

    def give_max_lockstones(self):
        PlayerLockstone(None, self.id, LockstoneList.basic_lockstone.name, 999).insert()
        PlayerLockstone(None, self.id, LockstoneList.elemental_lockstone.name, 999).insert()
        PlayerLockstone(None, self.id, LockstoneList.celestial_lockstone.name, 999).insert()
        PlayerLockstone(None, self.id, LockstoneList.esoteric_lockstone.name, 999).insert()
        PlayerLockstone(None, self.id, LockstoneList.arcanum_lockstone.name, 999).insert()
        PlayerLockstone(None, self.id, LockstoneList.divine_lockstone.name, 999).insert()

    def insert(self):
        with SQLiteConnector() as cur:
            query = '''
                INSERT INTO player (name, money)
                VALUES (?, ?)
            '''
            values = (self.name, self.money)
            cur.execute(query, values)
            self.id = cur.lastrowid

    def update(self):
        with SQLiteConnector() as cur:
            query = '''
                UPDATE player
                SET name = ?, money = ?
                WHERE id = ?
            '''
            values = (self.name, self.money, self.id)
            cur.execute(query, values)

    @classmethod
    def delete(cls, id):
        with SQLiteConnector() as cur:
            query = f"DELETE FROM player WHERE id = ?"
            values = (id,)
            cur.execute(query, values)