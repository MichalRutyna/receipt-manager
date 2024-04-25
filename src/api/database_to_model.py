from src.store_database import StoreDatabase
from src.load_config import TABLES_TRANSLATIONS, COLUMNS_TRANSLATIONS


def get_table_data(database: str, table: str, columns: list[str]) -> list[list]:

    #   REDIRECTION TO SUBFUCTIONS FOR EACH TABLE
    if table == _("store_items"):
        return get_store_item_table(database, columns)

    table = TABLES_TRANSLATIONS.get(table)
    with StoreDatabase(database) as db:
        db.cursor.execute(f'SELECT * FROM {table}')
        data = db.cursor.fetchall()
    return data


def get_store_item_table(database: str, columns: list[str]) -> list[list]:
    """
    Special columns:
        name

    """
    add_join = False
    query_str = "SELECT "
    args = []

    formatted_columns = columns.copy()
    formatted_columns = [COLUMNS_TRANSLATIONS[column] for column in formatted_columns]
    if 'name' in formatted_columns:
        add_join = " LEFT JOIN products on store_items.product_id = products.product_id"

    for column in formatted_columns:
        query_str += column + ", "
    query_str = query_str[:-2]

    query_str += " FROM store_items"

    if add_join:
        query_str += add_join

    with StoreDatabase(database) as db:
        print(query_str)
        db.cursor.execute(query_str, args)
        data = db.cursor.fetchall()
        print(data)
    return data
