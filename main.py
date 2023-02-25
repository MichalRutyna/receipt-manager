import pandas as pd
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
        if self.category_query(c) is False:
            return
        new_item = Item(name=a, mean_price=b, category=c)
        self.append_item(new_item)

    def category_query(self, query: str) -> bool:
        query = query.lower().capitalize()
        if query in self.category_list:
            return True
        else:
            if self.create_category(query):
                return self.category_query(query)
            else:
                print("Wystąpił błąd przy wyszukiwaniu kategorii!")
                return False

    def create_category(self, name) -> bool:
        try:
            if any(char in ("!", "@", "#", "$", "%", "^", "&", "*", "(", ")") for char in name):
                raise ValueError
            self.category_list.append(name.lower().capitalize())
            return True
        except ValueError:
            print("Wprowadzono nieprawidłową nazwę kategorii")
            return False


def test(baza_przedmiotow):
    assert baza_przedmiotow.category_query(baza_przedmiotow.category_list[0]) is True
    assert baza_przedmiotow.create_category("!@#baza") is False


def main():
    baza_przedmiotow = Lookup('lookup.csv')
    baza_zakupow = Database('data.csv')

    test(baza_przedmiotow)

    print("Witaj w bazie danych!")
    while True:
        print("-" * 50, "\nCo chcesz zrobić?: ")
        choice = input("(1 - wyświetl dane, 2 - wpisz nowy zakup, 3 - statystyki, q - wyjście): ")
        match choice:
            case '1':
                print("Twoje dane:\n")
                baza_zakupow.print_head(10)
            case '2':
                print("Wprowadzanie nowego zakupu: \n")
                item_queried = None
                while item_queried is None:
                    name_query = input("Podaj nazwę produktu: ")
                    item_queried = baza_przedmiotow.find_item(name_query)
                    if item_queried is None:
                        if input("Nie znaleziono takiego przedmiotu."
                                 " Chcesz utworzyć nowy przedmiot, czy spróbować ponownie? (1/2): ") == 2:

                            baza_przedmiotow.create_item()
                baza_zakupow.append_purchase([Purchase(item=item_queried,
                                                       price=float(input("Podaj cenę produktu: ")),
                                                       store=input("Podaj sklep: "),
                                                       date=datetime.date.today())])
            case '3':
                nazwa = input("Nazwa produktu: ")
                przedmiot = baza_przedmiotow.find_item(nazwa)
                print("-" * 50)
                print("Kategoria tego produktu to: ", przedmiot.category)
                print("Średnia cena tego produktu to: ", przedmiot.mean_price)

            case 'test':
                pass

            case 'q':
                break


if __name__ == '__main__':
    main()
