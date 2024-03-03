import tkinter
from tkinter import ttk

import pandas
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import src.building_classes.gui_parts as gui
from src.building_classes.shopping_databases_depreciated import *

from typing import Dict, Tuple


def GUI():
    root = gui.Root()
    main_window = gui.Window(root)
    window_functionality(main_window, root)
    content_label = base_gui(main_window)
    create_plots(content_label)
    root.mainloop()


def create_scenes(content_label: tkinter.Label) -> Tuple[Dict[str, tkinter.Label], Dict[str, str]]:
    """
    content_label: master of scene labels

    returns:
    - dict containing scene labels indexed by id
    - dict containing scene full names indexed by id


    Adding an item here will NOT create a new scene
    """
    scenes = {"home": tkinter.Label(content_label, bg='red'),
              "database": tkinter.Label(content_label, bg='blue'),
              "plots": tkinter.Label(content_label, bg='green'),
              "new purchase": tkinter.Label(content_label, bg='yellow')}

    scene_names = {"home": "Strona główna",
                   "database": "Baza danych",
                   "plots": "Wykresy",
                   "new purchase": "Nowy zakup"}

    return scenes, scene_names


def window_functionality(master: gui.Window, root) -> None:
    """
    Adds a title bar to a window containing window control buttons
    """
    title_bar = gui.Title_bar(master)
    title_bar.pack(side='top', fill='x')

    title = tkinter.Label(title_bar, image=master.ikona, text=master.wm_title(), fg='white', bg=title_bar['bg'],
                          padx='5px', compound='left')
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


def base_gui(master: gui.Window) -> tkinter.Label:
    """
    Creates the skeleton of the GUI
    """

    # small strip on the right
    quick_acces = tkinter.Label(master, bg='#333000', width=3)

    # main navigation on the left
    navigation = tkinter.Label(master, bg='#333333', width=12)

    # main content
    content = tkinter.Label(master, bg='#222222')
    content.state = "home"
    scenes, scene_names = create_scenes(content)

    def change_scene(scene_id):
        if content.state != scene_id:
            for child in content.winfo_children():
                child.pack_forget()
            scenes[scene_id].pack(expand=True, fill='both')
            content.state = scene_id

    for sceneId, sceneName in scene_names.items():
        print(sceneId)
        (gui.Button(navigation, "#333333", height=2, text=sceneName,
                   command=lambda new_scene=sceneId: change_scene(new_scene))
         .pack(side='top', fill='x'))

    style = ttk.Style()
    style.configure("Grip.TSizegrip", background=quick_acces['bg'])
    grip = ttk.Sizegrip(quick_acces, style="Grip.TSizegrip")
    grip.place(relx=1.0, rely=1.0, anchor="se")

    quick_acces.pack(side='right', fill='y')
    navigation.pack(side='left', fill='y')
    content.pack(fill='both', expand=100)

    return content


def create_plots(master):
    """Temporary function"""
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
