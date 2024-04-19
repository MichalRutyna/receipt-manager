from src.store_database import StoreDatabase
from src.load_config import TABLES_TRANSLATIONS


def get_table_data(database: str, table: str) -> list[list]:
    table = TABLES_TRANSLATIONS.get(table)

    # TODO getting data
    with StoreDatabase(database) as db:
        db.cursor.execute(f'SELECT * FROM {table}')
        data = db.cursor.fetchall()
    print("data:\n" + repr(data) )
    return data
