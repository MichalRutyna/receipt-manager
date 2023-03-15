import datetime
import logging
import tkinter
from tkinter import ttk
import classes.gui as gui
from classes.databases import Lookup, Purchase_base
from classes.dataclasses import Purchase
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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


def init_func_frame(master: gui.Window, root):
    title_bar = gui.Title_bar(master)
    title_bar.pack(side='top', fill='x')

    title = tkinter.Label(title_bar, image=master.ikona, text=master.wm_title(), fg='gray', bg='black', padx='5px', compound='left')
    close_button = gui.Button(title_bar, "#FF0000", text=chr(0x72), font='Marlett', width=5, bg='black', borderwidth=0,
                              command=lambda: root.destroy(), )
    maximize_button = gui.Button(title_bar, "#FF0000", text=chr(0x32), font='Marlett', width=3, bg='black', borderwidth=0,
                                 command=lambda: master.malize())
    inconify_button = gui.Button(title_bar, "#FF0000", text=chr(0x30), font='Marlett', width=3, bg='black', borderwidth=0,
                                 command=lambda: root.iconify())
    title.pack(side='left')
    close_button.pack(side='right')
    maximize_button.pack(side='right')
    inconify_button.pack(side='right')

    style = ttk.Style()
    style.configure("Grip.TSizegrip", background="#121212")
    grip = ttk.Sizegrip(master, style="Grip.TSizegrip")
    grip.place(relx=1.0, rely=1.0, anchor="se")


def GUI():
    root = gui.Root()
    main_window = gui.Window(root)
    init_func_frame(main_window, root)
    container = tkinter.Label(main_window, bg='#121212')

    navigation = tkinter.Label(container, bg='#333333', width=12)
    navigation_buttons = [home := gui.Button(navigation, "#333333", height=2, text="Strona główna"),
                          data_list := gui.Button(navigation, "#333333", height=2, text="Wyświetl bazę danych"),
                          graphs := gui.Button(navigation, "#333333", height=2, text="Pokaż wykresy"),
                          new_purchases := gui.Button(navigation, "#333333", height=2, text="Dodaj nowy zakup")]
    for button in navigation_buttons:
        button.pack(side='top', fill='x')

    content = tkinter.Label(container, bg='#222222')
    content.state = "home"

    navigation.pack(side='left', fill='y')
    content.pack(fill='both', expand=100)
    container.pack(fill='both', expand=999)
    root.mainloop()


def create_plots():
    baza_przedmiotow = Lookup('data/lookup.csv')
    baza_zakupow = Purchase_base('data/data.csv')

    plt.pie(baza_przedmiotow.df["Median_price"],
            labels=baza_przedmiotow.df["Name"])
    plt.show()


def main():

    # logging.basicConfig(level=logging.DEBUG,
    #                     filename='logs/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    console_ui()


if __name__ == '__main__':
    main()
