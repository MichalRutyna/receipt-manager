import pickle


def test_to_files(filename: str) -> None:
    with open(f"data/{filename}", "w", encoding="utf-8") as file:
        file.write(str(filename))
    with open(f"data/{filename}.pkl", "wb") as f:
        pickle.dump(filename, f)


def print_column_list(db):
    from src.store_database import StoreDatabase
    with StoreDatabase(db) as db:
        db.cursor.execute("SELECT * FROM PRAGMA_TABLE_LIST()")
        table_list = []
        for table in db.cursor.fetchall():
            table_list.append(table[1])
        for dev in ['test', 'sqlite_schema', 'sqlite_temp_schema', 'sqlite_sequence']:
            table_list.remove(dev)

        string = "{\n"
        for table in table_list:
            db.cursor.execute("SELECT * FROM PRAGMA_TABLE_INFO(?)", [table])
            string += "_('" + table + "'):\n[\n"
            for column in db.cursor.fetchall():
                string += "_('" + column[1] + "'),\n"
            string += "],\n"
        string += '}'
    print(string)