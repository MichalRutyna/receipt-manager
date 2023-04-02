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

    title = tkinter.Label(title_bar, image=master.ikona, text=master.wm_title(), fg='white', bg=title_bar['bg'], padx='5px', compound='left')
    close_button = gui.Button(title_bar, "#FF0000", text=chr(0x72), font='Marlett', fg='#CCCCCC', width=5,
                              bg=title_bar['bg'], borderwidth=0, command=lambda: root.destroy(), )
    maximize_button = gui.Button(title_bar, "#555555", text=chr(0x32), font='Marlett', fg='#CCCCCC', width=3,
                                 bg=title_bar['bg'], borderwidth=0, command=lambda: master.malize())
    inconify_button = gui.Button(title_bar, "#555555", text=chr(0x30), font='Marlett', fg='#CCCCCC', width=3,
                                 bg=title_bar['bg'], borderwidth=0, command=lambda: root.iconify())
    title.pack(side='left')
    close_button.pack(side='right')
    maximize_button.pack(side='right')
    inconify_button.pack(side='right')


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

    quick_acces = tkinter.Label(main_window, bg='#333333', width=3)

    style = ttk.Style()
    style.configure("Grip.TSizegrip", background=quick_acces['bg'])
    grip = ttk.Sizegrip(quick_acces, style="Grip.TSizegrip")
    grip.place(relx=1.0, rely=1.0, anchor="se")

    quick_acces.pack(side='right', fill='y')
    navigation.pack(side='left', fill='y')
    content.pack(fill='both', expand=100)
    create_plots(main_window)
    root.mainloop()


def create_plots(master):
    baza_przedmiotow = Lookup('data/lookup.csv')
    baza_zakupow = Purchase_base('data/data.csv')
    data1 = {'country': ['A', 'B', 'C', 'D', 'E'],
             'gdp_per_capita': [45000, 42000, 52000, 49000, 47000]
             }
    df1 = pandas.DataFrame(data1)

    figure2 = plt.Figure(figsize=(5, 4), dpi=100)
    ax2 = figure2.add_subplot(111)

    widget = FigureCanvasTkAgg(figure2, master)
    widget.get_tk_widget().pack()

    ax2.pie(baza_przedmiotow.df["Median_price"])

    # figure1 = plt.Figure(figsize=(6, 5), dpi=100)
    # ax1 = figure1.add_subplot(111)
    # bar1 = FigureCanvasTkAgg(figure1, master)
    # bar1.get_tk_widget().pack(side='left', fill='both')
    # df1 = df1[['country', 'gdp_per_capita']].groupby('country').sum()
    # df1.plot(kind='bar', legend=True, ax=ax1)
    # ax1.set_title('Country Vs. GDP Per Capita')


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
