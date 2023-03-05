import pandas as pd
from typing import List
from classes.dataclasses import Item, Purchase


class Purchase_base:
    def __init__(self, path):
        self.path = path
        self.columns = ["price", "store", "date"]
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        self.df = pd.read_csv(self.path)

    def print_head(self, rows):
        print(self.df.head(rows))

    def append_purchase(self, items: List[Purchase]) -> None:
        """
        Appends a list of Purchases to the database
        :param items:
        :return:
        """
        items = [[purchase.item.name, purchase.price, purchase.store, purchase.date] for purchase in items]
        thing_to_save = pd.DataFrame(items)
        thing_to_save.to_csv(self.path, mode='a', header=False, index=False)
        self.df = pd.read_csv(self.path)  # refresh


class Lookup:
    def __init__(self, path):
        self.path = path
        self.df = pd.read_csv(self.path)
        self.category_list = self.get_category_list()

    def get_category_list(self) -> List:
        return pd.factorize(self.df['Category'])[1].tolist()

    def find_item(self, name):
        idx, names = pd.factorize(self.df['Name'])
        item_index = names.get_indexer([name])[0]
        if item_index == -1:
            print("Nie znaleziono pasującego przedmiotu")
            return None
        item_as_list = self.df.iloc[item_index].to_list()
        return Item(name=item_as_list[0],
                    mean_price=item_as_list[1],
                    category=item_as_list[2])

    def append_item(self, item: Item) -> None:
        item = [item.name, item.category, item.mean_price]
        thing_to_save = pd.DataFrame(item)
        thing_to_save.to_csv(self.path, mode='a', header=False, index=False)

    def create_item(self) -> None:
        a = input("Podaj nazwę: ")
        b = -1  # TODO obsługa mean_price
        c = input("Podaj kategorię: ")
        self.category_query(c)

        new_item = Item(name=a, mean_price=b, category=c)
        self.append_item(new_item)

    def category_query(self, query: str) -> None:
        query = query.lower().capitalize()
        if query not in self.category_list:
            self.create_category(query)

    def create_category(self, name) -> None:
        if any(char in ("!", "@", "#", "$", "%", "^", "&", "*", "(", ")") for char in name):
            raise ValueError("Unallowed characters in category name")
        self.category_list.append(name.lower().capitalize())
