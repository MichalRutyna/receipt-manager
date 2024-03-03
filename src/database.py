import sqlite3

class Database:
    """
    Interface for interacting with the database made into a class because the user can switch databases
    This class is the owner of the reference to the sqlite database
    """

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.database = sqlite3.connect(f'{self.name}.db')
        self.cursor = self.database.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO exc logging
        self.cursor.close()
        self.database.close()

    def create_empty_database(self) -> None:
        self.cursor.execute('create table test (id INTEGER PRIMARY KEY, name TEXT, price DOUBLE)')
