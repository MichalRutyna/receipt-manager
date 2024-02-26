import datetime
import logging
from shopping_databases import Lookup, Purchase_base
from shopping_dataclasses import Purchase
from database import Database

import gui


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

import sqlite3 as sql
def create_database() -> None:
    db = sql.connect("test.db")
    cu = db.cursor()
    cu.execute("create table test (id INTEGER PRIMARY KEY, name TEXT, price DOUBLE)")

    db.close()

def test():
    with Database("test") as db:
        db.create_empty_database()

def main():
    gui.GUI()


if __name__ == '__main__':
    test()
