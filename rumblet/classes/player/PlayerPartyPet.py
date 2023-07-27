from rumblet.classes.db.SQLiteConnector import SQLiteConnector
from rumblet.classes.db.SQLiteSchema import SQLiteSchema
from rumblet.classes.pet.Pet import Pet

class PlayerPartyPet:
    table = SQLiteSchema.table_playerpartypet

    def __init__(
            self,
            id,
            player_id,
            pet_id,
            slot_number
    ):
        self.id = id
        self.player_id = player_id
        self.pet_id = pet_id
        self.slot_number = slot_number

    def insert(self):
        with SQLiteConnector() as cur:
            query = '''
                INSERT INTO playerpartypet (player_id, pet_id, slot_number)
                VALUES (?, ?, ?)
            '''
            values = (
                self.player_id,
                self.pet_id,
                self.slot_number
            )
            cur.execute(query, values)
            self.id = cur.lastrowid

    def update(self):
        with SQLiteConnector() as cur:
            query = '''
                UPDATE playerpartypet
                SET player_id = ?, pet_id = ?, slot_number = ?
                WHERE id = ?
            '''
            values = (
                self.player_id,
                self.pet_id,
                self.slot_number,
                self.id
            )
            cur.execute(query, values)

    @classmethod
    def delete(cls, id):
        with SQLiteConnector() as cur:
            query = f"DELETE FROM playerpartypet WHERE id = ?"
            values = (id,)
            cur.execute(query, values)

    @classmethod
    def get_party_by_player_id(cls, player_id):
        pets = Pet.get_all()
        with SQLiteConnector() as cur:
            query = "SELECT * FROM playerpartypet WHERE player_id = ?"
            values = (player_id,)
            cur.execute(query, values)
            rows = cur.fetchall()

            party = dict()
            for row in rows:
                slot_number = row[cls.table.get_column_index_by_name("slot_number")]
                pet = pets.get(row[cls.table.get_column_index_by_name("pet_id")])
                party[slot_number] = pet

            return party

    @classmethod
    def get_by_player_id_and_slot_number(cls, player_id, slot_number):
        with SQLiteConnector() as cur:
            query = "SELECT * FROM playerpartypet WHERE player_id = ? AND slot_number = ?"
            values = (player_id, slot_number)
            cur.execute(query, values)
            row = cur.fetchone()
            if row:
                return PlayerPartyPet(
                    id=row[cls.table.get_column_index_by_name("id")],
                    player_id=row[cls.table.get_column_index_by_name("player_id")],
                    pet_id=row[cls.table.get_column_index_by_name("pet_id")],
                    slot_number=row[cls.table.get_column_index_by_name("slot_number")]
                )
            return None

    @classmethod
    def next_available_party_slot_by_player_id(cls, player_id):
        party = cls.get_party_by_player_id(player_id)
        available_slot_numbers = [slot_number for slot_number, pet in party.items() if pet is None]
        next_available_slot_number = max(available_slot_numbers) + 1
        return next_available_slot_number if next_available_slot_number <= 6 else None
