import base64
import datetime
import logging
import os

import src.gui as gui
from src.building_classes.shopping_databases_depreciated import Lookup, Purchase_base
from src.building_classes.shopping_dataclasses_depreciated import Purchase
from src.database import Database


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
    with Database("test") as db:
        db.select_item_list(sort_by="sddsd", descending=True)


def test_api():
    import requests
    import json
    import string

    CLIENT_ID = "LidlPlusNativeClient"

    try:
        with open("data/token2", mode='r') as token_save_file:
            lidl_data = json.loads(token_save_file.read())
            _refresh_token = lidl_data["refresh_token"]
            _access_token = lidl_data["access_token"]
    except Exception as e:
        with open("data/token", mode='r') as token_backup:
            lidl_data = json.loads(token_backup.read())
            _refresh_token = lidl_data["refresh_token"]
            _access_token = lidl_data["access_token"]
        print(e)

    secret = base64.b64encode(f"{CLIENT_ID}:secret".encode()).decode()
    response = requests.post("https://accounts.lidl.com/connect/token",
                             headers={'Content-Type': 'application/x-www-form-urlencoded',
                                      'Authorization': f'Basic {secret}'},
                             data={'grant_type': 'refresh_token', "refresh_token": _refresh_token}).json()
    # print(response)

    with open("data/token2", mode='w') as token_save_file:
        save_data = str(response).replace("'", "\"")
        token_save_file.write(save_data)

    _refresh_token = response["refresh_token"]
    _access_token = response["access_token"]
    _get_recepits(_access_token)


def _get_recepits(token):
    import requests

    headers = {'Authorization': f'Bearer {token}',
               'App-Version': '999.99.9',
               'Operating-System': 'iOS',
               'App': 'com.lidl.eci.lidl.plus'}

    response = requests.get("https://tickets.lidlplus.com/api/v1/NL/list/1", headers=headers)
    print(response)


def main():
    gui.GUI()


if __name__ == '__main__':
    logging_innit()
    test_api()
