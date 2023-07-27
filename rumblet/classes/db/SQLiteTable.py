class SQLiteTable:
    def __init__(self, name, columns, foreign_keys=None):
        self.name = name
        self.columns = columns
        self.foreign_keys = foreign_keys or list()

    def get_column_index_by_name(self, column_name):
        return self.columns.get(column_name).get("index")

    def create_statement(self):
        structure = ', '.join([column_details.get("statement") for column_details in self.columns.values()] + self.foreign_keys)
        return f"CREATE TABLE IF NOT EXISTS {self.name} ({structure});"
