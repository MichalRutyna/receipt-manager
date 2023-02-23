import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import pydantic
from typing import List


class Item(pydantic.BaseModel):
    """
    Represents items known

    Item(name: str,
        median_price: float,

        category: str)
    """
    name: str
    mean_price: float
    category: str


class Purchase(pydantic.BaseModel):
    """
    Represents individual purchase

    Purchase(item: Item,
        price: float,

        store: str,

        date: datetime.date)
    """
    item: Item
    price: float
    store: str
    date: datetime.date


class Database:
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

    def append_item(self, item: Item):
        item = [item.name, item.category, item.mean_price]
        thing_to_save = pd.DataFrame(item)
        thing_to_save.to_csv(self.path, mode='a', header=False, index=False)


def main():
    baza_przedmiotow = Lookup('lookup.csv')
    baza_zakupow = Database('data.csv')

    print("Witaj w bazie danych!")
    while True:
        print("-" * 50, "\nCo chcesz zrobić?: ")
        choice = input("(1 - wyświetl dane, 2 - wpisz nowy zakup, 3 - statystyki, q - wyjście): ")
        match choice:
            case '1':
                print("Twoje dane:\n")
                baza_zakupow.print_head(10)
            case '2':
                chleb = Item(name="Ser", median_price=19.99, category="Essentials")
                print("Wprowadzanie nowego zakupu: \n")
                baza_zakupow.append_purchase([Purchase(item=chleb,
                                                       price=float(input("Podaj cenę produktu: ")),
                                                       store=input("Podaj sklep: "),
                                                       date=datetime.date.today())])
            case '3':
                nazwa = input("Nazwa produktu: ")
                print("-" * 50)
                print("Kategoria tego produktu to: ", baza_przedmiotow.check_category(nazwa))
                print("Średnia cena tego produktu to: ", baza_przedmiotow.check_category(nazwa))

            case 'test':
                print(baza_przedmiotow.test("Ser"))

            case 'q':
                break


if __name__ == '__main__':
    main()
