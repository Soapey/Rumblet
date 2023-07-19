import sqlite3
import os
from rumblet.classes.utils import root_directory

DB_NAME = "rumblet.sql"

class SQLiteConnector:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connect()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit_changes()
        self.disconnect()

    def connect(self):
        self.connection = sqlite3.connect(DB_NAME)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.connection.cursor()

    def commit_changes(self):
        self.connection.commit()

    def disconnect(self):
        self.cursor.close()
        self.connection.close()

def initialise_db():
    root_path = root_directory()
    init_file_path = os.path.join(root_path, "rumblet", "init.sql")
    with open(init_file_path, "r") as init_file:
        sql_script = init_file.read()
        with SQLiteConnector() as cur:
            cur.executescript(sql_script)
