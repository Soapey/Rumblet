from rumblet.classes.db.SQLiteConnector import SQLiteConnector
from rumblet.classes.db.SQLiteSchema import SQLiteSchema


class PlayerBagItem:
    table = SQLiteSchema.table_playerbagitem

    def __init__(
            self,
            id,
            player_id,
            bag_item_name,
            quantity
    ):
        self.id = id
        self.player_id = player_id
        self.bag_item_name = bag_item_name
        self.quantity = quantity

    def insert(self):
        with SQLiteConnector() as cur:
            query = '''
                INSERT INTO playerbagitem (player_id, bag_item_name, quantity)
                VALUES (?, ?, ?)
            '''
            values = (
                self.player_id,
                self.bag_item_name,
                self.quantity
            )
            cur.execute(query, values)
            self.id = cur.lastrowid

    def update(self):
        with SQLiteConnector() as cur:
            query = '''
                UPDATE playerbagitem
                SET player_id = ?, bag_item_name = ?, quantity = ?
                WHERE id = ?
            '''
            values = (
                self.player_id,
                self.bag_item_name,
                self.quantity,
                self.id
            )
            cur.execute(query, values)

    def set_item_quantity(self, quantity):
        self.quantity = quantity
        self.update()

    @classmethod
    def delete(cls, id):
        with SQLiteConnector() as cur:
            query = f"DELETE FROM playerbagitem WHERE id = ?"
            values = (id,)
            cur.execute(query, values)

    @classmethod
    def get_all_by_player_id(cls, player_id):
        with SQLiteConnector() as cur:
            query = '''
            SELECT * FROM playerbagitem
            WHERE player_id = ?
            '''
            values = (player_id,)
            cur.execute(query, values)
            rows = cur.fetchall()
            bag = dict()
            for row in rows:
                bag_item_name = row[cls.table.get_column_index_by_name("bag_item_name")]
                bag[bag_item_name] = PlayerBagItem(
                    id=row[cls.table.get_column_index_by_name("id")],
                    player_id=row[cls.table.get_column_index_by_name("player_id")],
                    bag_item_name=bag_item_name,
                    quantity=row[cls.table.get_column_index_by_name("quantity")]
                )


    @classmethod
    def get_by_player_id_and_name(cls, player_id, bag_item_name):
        with SQLiteConnector() as cur:
            query = '''
            SELECT * FROM playerbagitem
            WHERE player_id = ? AND bag_item_name = ?
            '''
            values = (player_id, bag_item_name)
            cur.execute(query, values)
            row = cur.fetchone()
            return PlayerBagItem(
                    id=row[cls.table.get_column_index_by_name("id")],
                    player_id=row[cls.table.get_column_index_by_name("player_id")],
                    bag_item_name=bag_item_name,
                    quantity=row[cls.table.get_column_index_by_name("quantity")]
                )
