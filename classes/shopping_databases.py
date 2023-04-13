import logging
import pandas as pd
from typing import List, Optional
from classes.shopping_dataclasses import Item, Purchase


class Purchase_base:
    def __init__(self, path):
        self.path = path
        self.columns = ["price", "store", "date"]
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        self.df = pd.read_csv(self.path)
        logging.info(f"Initialized Purchase database at {self.path}")

    def print_head(self, rows: int) -> None:
        print(self.df.head(rows))

    def append_purchase(self, items: List[Purchase]) -> None:
        """
        Appends a list of Purchases to the database
        :param items:
        :return:
        """
        items = [[purchase.item.name, purchase.price, purchase.amount, purchase.store, purchase.date] for purchase in items]
        thing_to_save = pd.DataFrame(items)
        thing_to_save.to_csv(self.path, mode='a', header=False, index=False)
        self.df = pd.read_csv(self.path)  # refresh
        logging.debug(f"Appended Purchase: {items}")


class Lookup:
    def __init__(self, path: str):
        self.path = path
        self.df = pd.read_csv(self.path)
        self.category_list = self.get_category_list()
        logging.info(f"Initialized Lookup database at {self.path}")

    def get_category_list(self) -> List:
        return pd.factorize(self.df['Category'])[1].tolist()

    def find_item(self, name: str) -> Optional[Item]:
        self.df = pd.read_csv(self.path)
        idx, names = pd.factorize(self.df['Name'])
        item_index = names.get_indexer([name])[0]
        if item_index == -1:
            return None
        item_as_list = self.df.iloc[item_index].to_list()
        return Item(name=item_as_list[0],
                    mean_price=item_as_list[1],
                    category=item_as_list[2])

    def append_item(self, item: Item) -> None:
        itm = [item.name, item.mean_price, item.category]
        thing_to_save = pd.DataFrame(itm)
        thing_to_save.transpose().to_csv(self.path, mode='a', header=False, index=False, sep=',')
        self.df = pd.read_csv(self.path)
        logging.debug(f"Appended Item: {item}")

    def create_item(self) -> None:
        # TODO create item by parameters
        a = input("Podaj nazwę: ")
        b = -1  # TODO obsługa mean_price
        c = input("Podaj kategorię: ")

        new_item = Item(name=a, mean_price=b, category=c)
        self.append_item(new_item)
        self.df = pd.read_csv(self.path)
        logging.info(f"Created new Item: {new_item}")

    # def category_query(self, query: str) -> None:
    #     query = query.lower().capitalize()
    #     if query not in self.category_list:
    #         self.create_category(query)
    #
    # def create_category(self, name: str) -> None:
    #     if any(char in "!@#$%^&*()" for char in name):
    #         raise ValueError("Unallowed characters in category name")
    #     self.category_list.append(name.lower().capitalize())
    #     logging.info(f"Created new category: {name.lower().capitalize()}")
