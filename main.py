import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import pydantic
from typing import Union, List


class Item(pydantic.BaseModel):
    name: str
    price: float
    category: str
    store: str
    date: datetime.date

    def __repr_args__(self):
        print("called __repr_args__")
        return [(None, value) for key, value in self.__dict__.items()]


class Database:
    def __init__(self, path):
        self.path = path
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        self.df = pd.read_csv(self.path)

    def print_head(self, rows):
        print(self.df.head(rows))

    def append_item(self, item: List[Item]):
        thing_to_save = pd.DataFrame([s.__dict__ for s in item])
        thing_to_save.to_csv(self.path, mode='a', header=False, index=False)
        # refresh
        self.df = pd.read_csv(self.path)

    def get_avg_price(self, name):
        counter = 0
        price_sum = 0
        for index, value in self.df['Price'].where(self.df['Name'] == name.capitalize()).dropna().items():
            counter += 1
            price_sum += float(value.replace(',', '.'))
        if counter == 0:
            return None
        else:
            return format(price_sum / counter, '.2f')


class Lookup:
    def __init__(self, path):
        self.path = path
        self.df = pd.read_csv(self.path, sep=";")

    def check_category(self, name):
        return self.df['Category'][self.df['Category'].where(self.df['Name'] == name.capitalize()).first_valid_index()]

    def append_item(self, name, category):
        thing_to_save: pd.DataFrame = pd.DataFrame(name, category)
        thing_to_save.to_csv(self.path, mode='a', sep=';', header=False, index=False)


def main():
    pass


if __name__ == '__main__':
    lookup = Lookup('lookup.csv')
    baza = Database('data.csv')

    # data.print_head(10)
    print("Witaj w bazie danych!")
    while True:
        print("-"*50, "\nCo chcesz zrobić?: ")
        choice = input("(1 - wyswietl dane, 2 - wpisz nowy zakup, 3 - statystyki, q - wyjscie): ")
        match choice:
            case '1':
                print("Twoje dane:\n")
                baza.print_head(10)
            case '2':
                print("Wprowadzanie nowej pozycji: \n")
                baza.append_item(name=input("Podaj nazwę: "),
                                 price=input("Podaj cenę: "),
                                 store=input("Podaj sklep: "),
                                 date=input("Podaj datę (jeśli nie dzisiaj)(DD.MM.RRRR): "))
            case '3':
                nazwa = input("Nazwa produktu: ")
                print("-"*50)
                print("Kategoria tego produktu to: ", lookup.check_category(nazwa))
                print("Średnia cena tego produktu to: ", baza.get_avg_price(nazwa))

            case 'test':
                x = np.linspace(0, 2 * np.pi, 200)
                y = np.sin(x)

                fig, ax = plt.subplots()
                ax.plot(x, y)
                plt.show()

            case 'x':
                chleb = Item(name="Ser", price=19.99, category="Essentials", store="Lidl", date=datetime.date.today())
                szynka = Item(name="Szynka", price=15.99, category="Essentials", store="Lidl", date=datetime.date.today())
                baza.append_item([chleb, szynka])

            case 'q':
                break
