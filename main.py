import datetime
import tkinter
from tkinter import ttk
from PIL import ImageTk, Image
import classes.gui as gui
from classes.databases import Lookup, Purchase_base
from classes.dataclasses import Purchase


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
                                                       store=input("Podaj sklep: "),
                                                       date=datetime.date.today())])
            case '3':
                nazwa = input("Nazwa produktu: ")
                przedmiot = baza_przedmiotow.find_item(nazwa)
                print("-" * 50)
                print("Kategoria tego produktu to: ", przedmiot.category)
                print("Średnia cena tego produktu to: ", przedmiot.mean_price)

            case 'test':
                baza_przedmiotow.create_item()

            case 'q':
                break


def init_func_frame(master, root):
    title_bar = gui.Title_bar(master)
    title_bar.pack(side='top', fill='x')

    title = tkinter.Label(title_bar, image=master.ikona, text=master.wm_title(), fg='gray', bg='black', padx='5px', compound='left')
    close_button = gui.Button(title_bar, "#FF0000", text='X', font='Inter 13', width=5, bg='black',
                              command=lambda: root.destroy(), )
    maximize_button = gui.Button(title_bar, "#FF0000", text=chr(0x32), font='Marlett', width=3, bg='black',
                                 command=lambda: master.malize())
    inconify_button = gui.Button(title_bar, "#FF0000", text=chr(0x30), font='Marlett', width=3, bg='black',
                                 command=lambda: root.iconify())
    title.pack(side='left')
    close_button.pack(side='right')
    maximize_button.pack(side='right')
    inconify_button.pack(side='right')

    style = ttk.Style()
    style.configure("Grip.TSizegrip", background="#121212")
    grip = ttk.Sizegrip(master, style="Grip.TSizegrip")
    grip.place(relx=1.0, rely=1.0, anchor="se")


def main():
    root = gui.Root()
    main_window = gui.Window(root)
    init_func_frame(main_window, root)

    content = tkinter.Label(main_window, bg='#121212')
    content.pack()

    root.mainloop()


if __name__ == '__main__':
    main()
