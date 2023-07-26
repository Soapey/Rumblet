CREATE TABLE IF NOT EXISTS player (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    current_zone_name TEXT NOT NULL,
    grid_cell_x INTEGER NOT NULL,
    grid_cell_y INTEGER NOT NULL,
    facing_direction INTEGER NOT NULL,
    money INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS playerbagitem (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    bag_item_name TEXT NOT NULL,
    quantity INTEGER NOT NULL
    FOREIGN KEY (player_id) REFERENCES player(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS pet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    species_name TEXT NOT NULL,
    level INTEGER NOT NULL,
    experience INTEGER NOT NULL,
    nickname TEXT,
    health INTEGER NOT NULL,
    defense INTEGER NOT NULL,
    attack INTEGER NOT NULL,
    speed INTEGER NOT NULL,
    current_health INTEGER NOT NULL,
    current_defense INTEGER NOT NULL,
    current_attack INTEGER NOT NULL,
    current_speed INTEGER NOT NULL,
    move_1_name TEXT,
    move_2_name TEXT,
    move_3_name TEXT,
    move_4_name TEXT,
    FOREIGN KEY (player_id) REFERENCES player(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS petmove (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pet_id INTEGER NOT NULL,
    move_name TEXT NOT NULL,
    current_fuel INTEGER NOT NULL,
    FOREIGN KEY (pet_id) REFERENCES pet(id) ON DELETE CASCADE
);