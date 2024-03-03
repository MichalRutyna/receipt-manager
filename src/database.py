import logging
import sqlite3


class Database:
    """
    Interface for interacting with the database made into a class because the user can switch databases
    This class is the owner of the reference to the sqlite database

    The proper use of the database is with python's context manager:
    with Database("name") as db:
        db.foo()
    """

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self._database = sqlite3.connect(f'{self.name}.db')
        self.cursor = self._database.cursor()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO exc logging
        self.cursor.close()
        self._database.close()

    def create_empty_database(self) -> None:
        self.cursor.execute('create table test (id INTEGER PRIMARY KEY, name TEXT, price DOUBLE)')

    def select_item_list(self, sort_by: str, descending: bool = False) -> None:
        """
        After selecting items from the database, there should be call(s) to db.cursor.fetch() in order to fetch the data
        """
        # TODO sort_by filtering (unexpected columns)
        if sort_by not in ('id', 'name', 'price'):
            logging.exception(f"Selection of items from databased was tried to be sorted by an invalid column! (\"{sort_by}\")")
            return

        command = f'select * from test order by {sort_by}'
        if descending:
            command += ' desc'

        self.cursor.execute(command)
