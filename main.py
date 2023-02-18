import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime


class Database:
    def __init__(self, path):
        self.path = path
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        self.df = pd.read_csv(self.path, sep=";", index_col='Id')

    def print_head(self, rows):
        print(self.df.head(rows))

    def append_item(self, name, price, date, store=None):
        # jeśli cena nie została podana, sprawdź średnią cenę
        if price == '':
            price = self.get_avg_price(name)

        # jeśli data nie została podana, weź aktualną datę
        if date == '':
            date = datetime.date.today().strftime('%d.%m.%Y')

        # sprawdź kategorię w tabeli
        category = lookup.check_category(name)

        # przygotuj tabelę do zapisu
        thing_to_save: pd.DataFrame = pd.DataFrame(self.df.index.max() + 1, name.capitalize(), price, category, store, date)

        # dopisz w formacie csv, bez nazw kolumn i bez automatycznego indexu
        thing_to_save.to_csv(self.path, mode='a', sep=';', header=False, index=False)

        # odśwież wczytaną tabelę
        self.df = pd.read_csv(self.path, sep=";", index_col='Id')

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
    data = Database('dane.csv')

    # data.print_head(10)
    print("Witaj w bazie danych!")
    while True:
        print("-"*50, "\nCo chcesz zrobić?: ")
        choice = input("(1 - wyswietl dane, 2 - wpisz nowy zakup, 3 - statystyki, q - wyjscie): ")
        match choice:
            case '1':
                print("Twoje dane:\n")
                data.print_head(10)
            case '2':
                print("Wprowadzanie nowej pozycji: \n")
                data.append_item(name=input("Podaj nazwę: "),
                                 price=input("Podaj cenę: "),
                                 store=input("Podaj sklep: "),
                                 date=input("Podaj datę (jeśli nie dzisiaj)(DD.MM.RRRR): "))
            case '3':
                nazwa = input("Nazwa produktu: ")
                print("-"*50)
                print("Kategoria tego produktu to: ", lookup.check_category(nazwa))
                print("Średnia cena tego produktu to: ", data.get_avg_price(nazwa))

            case 'test':
                x = np.linspace(0, 2 * np.pi, 200)
                y = np.sin(x)

                fig, ax = plt.subplots()
                ax.plot(x, y)
                plt.show()

            case 'q':
                break
