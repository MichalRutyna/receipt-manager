import datetime
import logging
import gettext

import gui.main_gui as gui
from src.building_classes.shopping_databases_depreciated import Lookup, Purchase_base
from src.building_classes.shopping_dataclasses_depreciated import Purchase
from src.store_database import StoreDatabase


def console_ui():
    baza_przedmiotow = Lookup('data/lookup.csv')
    baza_zakupow = Purchase_base('data/data.csv')

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
                                 " Chcesz utworzyć nowy przedmiot, czy spróbować ponownie? (1/2): ") == '1':
                            while True:
                                try:
                                    baza_przedmiotow.create_item()
                                except ValueError:
                                    if input("Wprowadzono nieprawidłową nazwę kategorii,"
                                             " czy chcesz spróbować ponownie? (t/n): ") == 'n':
                                        break
                                else:
                                    break
                baza_zakupow.append_purchase([Purchase(item=item_queried,
                                                       price=float(input("Podaj cenę produktu: ")),
                                                       amount=int(input("Podaj ilość: ")),
                                                       store=input("Podaj sklep: "),
                                                       date=datetime.date.today())])
            case '3':
                nazwa = input("Nazwa produktu: ")
                przedmiot = baza_przedmiotow.find_item(nazwa)
                print("-" * 50)
                print("Kategoria tego produktu to: ", przedmiot.category)
                print("Średnia cena tego produktu to: ", przedmiot.mean_price)

            case '4':
                print("\nTworzenie nowego przedmiotu: \n")
                baza_przedmiotow.create_item()

            case 'test':
                pass

            case 'q':
                break


def logging_innit():
    logging.basicConfig(level=logging.DEBUG,
                        filename='logs/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


def test():
    with StoreDatabase("test") as db:
        db.select_item_list(sort_by="sddsd", descending=True)


def main():
    import src.api.main_api as api

    source = api.LidlAPI()
    main_db = 'test'

    #db_integration.update_into_database(source, main_db)
    gui.GUI()


if __name__ == '__main__':
    domain = 'receiptmanager'
    localedir = './locales'
    locale = 'pl'
    en_i18n = gettext.translation(domain, localedir, fallback=True, languages=['en', 'pl'])
    en_i18n.install()
    print(_("Witaj world"))

    logging_innit()
    main()





