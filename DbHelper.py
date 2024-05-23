import sqlite3

class DbHelper:
    cursor = None

    def load_db(self, db_file):
        print(f"Loading: {db_file}")
        if self.cursor is not None:
            self.cursor.close()
        connection = sqlite3.connect(db_file)
        self.cursor = connection.cursor()

        tables = self.list_tables()
        print(tables)
        return tables

    def list_tables(self):
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        print(query)
        self.cursor.execute(query)
        return [row[0] for row in self.cursor.fetchall()]

    def query_table(self, table):
        query = f"SELECT * FROM {table}"
        print(query)
        self.cursor.execute(query)
        column_names = [name[0] for name in self.cursor.description]
        values = self.cursor.execute(query).fetchall()

        table_dictionary = [column_names]
        for i in range(len(values)):
            table_dictionary.append(values[i])
        return table_dictionary
