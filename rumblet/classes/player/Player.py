from rumblet.classes.db.SQLiteConnector import SQLiteConnector
from rumblet.classes.player.PlayerLockstone import PlayerLockstone
from rumblet.classes.lockstone.LockstoneList import LockstoneList

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

    def get_lockstone_by_name(self, lockstone_name):
        with SQLiteConnector() as cur:
            query = '''
                SELECT * FROM playerlockstone
                WHERE player_id = ? AND lockstone_name = ?
            '''
            values = (self.id, lockstone_name)
            cur.execute(query, values)
            row = cur.fetchone()
            playerlockstone = PlayerLockstone(*row)

            if not playerlockstone.count:
                return None

            return LockstoneList.lockstones.get(playerlockstone.lockstone_name)

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
