import datetime
import logging
import tkinter
from tkinter import ttk
import pandas
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

    navigation = tkinter.Label(main_window, bg='#333333', width=12)
    navigation_buttons = [home := gui.Button(navigation, "#333333", height=2, text="Strona główna"),
                          data_list := gui.Button(navigation, "#333333", height=2, text="Wyświetl bazę danych"),
                          graphs := gui.Button(navigation, "#333333", height=2, text="Pokaż wykresy"),
                          new_purchases := gui.Button(navigation, "#333333", height=2, text="Dodaj nowy zakup")]
    for button in navigation_buttons:
        button.pack(side='top', fill='x')

    content = tkinter.Label(main_window, bg='#222222')
    content.state = "home"

    navigation.pack(side='left', fill='y')
    content.pack(fill='both', expand=100)
    root.mainloop()


def create_plots():
    root = tkinter.Tk()
    baza_przedmiotow = Lookup('data/lookup.csv')
    baza_zakupow = Purchase_base('data/data.csv')
    data2 = {'year': [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010],
             'unemployment_rate': [9.8, 12, 8, 7.2, 6.9, 7, 6.5, 6.2, 5.5, 6.3]
             }
    df2 = pandas.DataFrame(data2)

    figure2 = plt.Figure(figsize=(5, 4), dpi=100)
    ax2 = figure2.add_subplot(111)
    line = FigureCanvasTkAgg(figure2, root)
    line.get_tk_widget().pack(side='left', fill='both')
    df2 = baza_przedmiotow.df["Median_price"]
    print(df2)
    root.mainloop()


def logging_innit():
    logging.basicConfig(level=logging.DEBUG,
                        filename='logs/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


def test():

    root = tkinter.Tk()

    pasek = tkinter.Label(root, bg='black')
    przycisk1 = tkinter.Label(root, width=20, height=5, bg='blue')
    przycisk2 = tkinter.Label(root, width=20, height=5, bg='red')
    content = tkinter.Label(root, width=20, height=20, bg='white')
    content_child = tkinter.Label(content, width=20, height=20, bg='gray')

    pasek.pack(anchor='n', fill='x')
    przycisk1.pack(anchor='nw', side='left', fill='none')
    przycisk2.pack(anchor='nw', side='left', fill='none')
    content.pack(anchor='ne', expand=True, fill='both')
    content_child.pack()
    root.mainloop()


def main():
    GUI()


if __name__ == '__main__':
    main()
