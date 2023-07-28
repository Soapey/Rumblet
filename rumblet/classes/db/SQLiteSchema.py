from rumblet.classes.db.SQLiteConnector import SQLiteConnector
from rumblet.classes.db.SQLiteTable import SQLiteTable


class SQLiteSchema:
    name = "rumblet.sql"
    tables = {
        "player": SQLiteTable(
            name="player",
            columns={
                "id": {
                    "index": 0,
                    "statement": "id INTEGER PRIMARY KEY AUTOINCREMENT",
                },
                "name": {
                    "index": 1,
                    "statement": "name TEXT NOT NULL",
                },
                "current_zone_name": {
                    "index": 2,
                    "statement": "current_zone_name TEXT NOT NULL",
                },
                "grid_cell_x": {
                    "index": 3,
                    "statement": "grid_cell_x INTEGER NOT NULL",
                },
                "grid_cell_y": {
                    "index": 4,
                    "statement": "grid_cell_y INTEGER NOT NULL",
                },
                "facing_direction": {
                    "index": 5,
                    "statement": "facing_direction INTEGER NOT NULL",
                },
                "money": {
                    "index": 6,
                    "statement": "money INTEGER NOT NULL",
                },
            }
        ),
        "playerbagitem": SQLiteTable(
            name="playerbagitem",
            columns={
                "id": {
                    "index": 0,
                    "statement": "id INTEGER PRIMARY KEY AUTOINCREMENT",
                },
                "player_id": {
                    "index": 1,
                    "statement": "player_id INTEGER NOT NULL",
                },
                "bag_item_name": {
                    "index": 2,
                    "statement": "bag_item_name TEXT NOT NULL",
                },
                "quantity": {
                    "index": 3,
                    "statement": "quantity INTEGER NOT NULL",
                },
            },
            foreign_keys=[
                "FOREIGN KEY (player_id) REFERENCES player(id) ON DELETE CASCADE",
            ],
        ),
        "pet": SQLiteTable(
            name="pet",
            columns={
                "id": {
                    "index": 0,
                    "statement": "id INTEGER PRIMARY KEY AUTOINCREMENT",
                },
                "player_id": {
                    "index": 1,
                    "statement": "player_id INTEGER NOT NULL",
                },
                "species_name": {
                    "index": 2,
                    "statement": "species_name TEXT NOT NULL",
                },
                "level": {
                    "index": 3,
                    "statement": "level INTEGER NOT NULL",
                },
                "experience": {
                    "index": 4,
                    "statement": "experience INTEGER NOT NULL",
                },
                "nickname": {
                    "index": 5,
                    "statement": "nickname TEXT",
                },
                "health": {
                    "index": 6,
                    "statement": "health INTEGER NOT NULL",
                },
                "defense": {
                    "index": 7,
                    "statement": "defense INTEGER NOT NULL",
                },
                "attack": {
                    "index": 8,
                    "statement": "attack INTEGER NOT NULL",
                },
                "speed": {
                    "index": 9,
                    "statement": "speed INTEGER NOT NULL",
                },
                "current_health": {
                    "index": 10,
                    "statement": "current_health INTEGER NOT NULL",
                },
                "current_defense": {
                    "index": 11,
                    "statement": "current_defense INTEGER NOT NULL",
                },
                "current_attack": {
                    "index": 12,
                    "statement": "current_attack INTEGER NOT NULL",
                },
                "current_speed": {
                    "index": 13,
                    "statement": "current_speed INTEGER NOT NULL",
                },
                "move_1_name": {
                    "index": 14,
                    "statement": "move_1_name TEXT",
                },
                "move_2_name": {
                    "index": 15,
                    "statement": "move_2_name TEXT",
                },
                "move_3_name": {
                    "index": 16,
                    "statement": "move_3_name TEXT",
                },
                "move_4_name": {
                    "index": 17,
                    "statement": "move_4_name TEXT",
                },
            },
            foreign_keys=[
                "FOREIGN KEY (player_id) REFERENCES player(id) ON DELETE CASCADE",
            ],
        ),
        "petmove": SQLiteTable(
            name="petmove",
            columns={
                "id": {
                    "index": 0,
                    "statement": "id INTEGER PRIMARY KEY AUTOINCREMENT",
                },
                "pet_id": {
                    "index": 1,
                    "statement": "pet_id INTEGER NOT NULL",
                },
                "move_name": {
                    "index": 2,
                    "statement": "move_name TEXT NOT NULL",
                },
                "current_fuel": {
                    "index": 3,
                    "statement": "current_fuel INTEGER NOT NULL",
                },
            },
            foreign_keys=[
                "FOREIGN KEY (pet_id) REFERENCES pet(id) ON DELETE CASCADE",
            ],
        ),
        "playerpartypet": SQLiteTable(
            name="playerpartypet",
            columns={
                "id": {
                    "index": 0,
                    "statement": "id INTEGER PRIMARY KEY AUTOINCREMENT"
                },
                "player_id": {
                    "index": 1,
                    "statement": "player_id INTEGER NOT NULL"
                },
                "pet_id": {
                    "index": 2,
                    "statement": "pet_id INTEGER"
                },
                "slot_number": {
                    "index": 3,
                    "statement": "slot_number INTEGER NOT NULL"
                }
            },
            foreign_keys=[
                "FOREIGN KEY (player_id) REFERENCES player(id) ON DELETE CASCADE",
                "FOREIGN KEY (pet_id) REFERENCES pet(id) ON DELETE CASCADE"
            ]
        )
    }
    table_player = tables.get("player")
    table_playerbagitem = tables.get("playerbagitem")
    table_pet = tables.get("pet")
    table_petmove = tables.get("petmove")
    table_playerpartypet = tables.get("playerpartypet")

    @classmethod
    def initialise(cls):
        with SQLiteConnector() as cur:
            for sqlite_table in cls.tables.values():
                cur.execute(sqlite_table.create_statement())
