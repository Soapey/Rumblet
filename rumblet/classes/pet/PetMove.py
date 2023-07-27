from rumblet.classes.move.MoveList import MoveList
from rumblet.classes.db.SQLiteConnector import SQLiteConnector
from rumblet.classes.db.SQLiteSchema import SQLiteSchema


class PetMove:
    table = SQLiteSchema.table_petmove

    def __init__(
            self,
            id: int | None,
            pet_id: int | None,
            move_name: str | None,
            current_fuel: int | None,
            pet=None
    ):
        self.id = id
        self.pet_id = pet_id
        self.move_name = move_name
        self.current_fuel = current_fuel

        self.pet = pet

    def use(self, using_pet, target_pet):
        move = MoveList.moves.get(self.move_name)
        if not move:
            return

        func = move.ability
        func(using_pet, target_pet)

    def insert(self):
        with SQLiteConnector() as cur:
            query = '''
                INSERT INTO petmove (pet_id, move_name, current_fuel)
                VALUES (?, ?, ?)
            '''
            values = (self.pet_id, self.move_name, self.current_fuel)
            cur.execute(query, values)
            self.id = cur.lastrowid

    def update(self):
        with SQLiteConnector() as cur:
            query = '''
                UPDATE petmove
                SET pet_id = ?, move_name = ?, current_fuel = ?
                WHERE id = ?
            '''
            values = (self.pet_id, self.move_name, self.current_fuel, self.id)
            cur.execute(query, values)

    @classmethod
    def delete(cls, id):
        with SQLiteConnector() as cur:
            query = "DELETE FROM petmove WHERE id = ?"
            values = (id,)
            cur.execute(query, values)

    @classmethod
    def get_by_pet_id_and_move_name(cls, pet_id, move_name):
        with SQLiteConnector() as cur:
            query = '''
                SELECT * FROM petmove
                WHERE pet_id = ? AND move_name = ?
            '''
            values = (pet_id, move_name)
            cur.execute(query, values)
            row = cur.fetchone()
            return PetMove(
                id=row[cls.table.get_column_index_by_name("id")],
                pet_id=row[cls.table.get_column_index_by_name("pet_id")],
                move_name=row[cls.table.get_column_index_by_name("move_name")],
                current_fuel=row[cls.table.get_column_index_by_name("current_fuel")]
            )
