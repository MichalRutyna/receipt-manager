import tkinter
from tkinter import ttk

import pandas
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import gui_parts as gui
from shopping_databases import Lookup, Purchase_base

from typing import Dict


def create_scenes(content_label) -> Dict[str, tkinter.Label]:
    scenes = {"home": tkinter.Label(content_label, bg='red'),
              "database": tkinter.Label(content_label, bg='blue'),
              "plots": tkinter.Label(content_label, bg='green'),
              "new purchase": tkinter.Label(content_label, bg='yellow')}
    return scenes


def window_functionality(master: gui.Window, root) -> None:
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


def base_gui(master: gui.Window) -> tkinter.Label:
    # easy place to add scenes
    scene_dict = {"home": "Strona główna",
                  "database": "Baza danych",
                  "plots": "Wykresy",
                  "new purchase": "Nowy zakup"}

    def change_scene(scene_id):
        if content.state != scene_id:
            for child in content.winfo_children():
                child.pack_forget()
            scenes[scene_id].pack(expand=True, fill='both')
            content.state = scene_id

    quick_acces = tkinter.Label(master, bg='#333333', width=3)
    navigation = tkinter.Label(master, bg='#333333', width=12)

    # create and pack buttons from scene_dict for easy scene addition
    for sceneId, sceneName in scene_dict.items():
        gui.Button(navigation, "#333333", height=2, text=sceneName,
                   command=lambda sceneId = sceneId: change_scene(sceneId)).pack(side='top', fill='x')

    content = tkinter.Label(master, bg='#222222')
    content.state = "home"
    scenes = create_scenes(content)

    style = ttk.Style()
    style.configure("Grip.TSizegrip", background=quick_acces['bg'])
    grip = ttk.Sizegrip(quick_acces, style="Grip.TSizegrip")
    grip.place(relx=1.0, rely=1.0, anchor="se")

    quick_acces.pack(side='right', fill='y')
    navigation.pack(side='left', fill='y')
    content.pack(fill='both', expand=100)

    return content


def GUI():
    root = gui.Root()
    main_window = gui.Window(root)
    window_functionality(main_window, root)
    content_label = base_gui(main_window)
    create_plots(content_label)
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
