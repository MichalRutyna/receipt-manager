import tkinter as tk
from tkinter import ttk

from src.internal.database_model import POSSIBLE_TABLES
from src.gui.data_view import DataView


def create_database_scene(parent: tk.Label, database: str) -> tk.Label:
    print(_("Witaj world"))
    scene = tk.Label(parent)

    selected_table = tk.StringVar()
    table_select = ttk.Combobox(scene, textvariable=selected_table)
    table_select['values'] = POSSIBLE_TABLES
    table_select['state'] = 'readonly'
    table_select.pack()

    # View
    data_view = DataView(scene)

    # Model
    from src.internal.database_model import DataModel
    data_model = DataModel(data_view, database)
    from src.load_config import DEFAULT_TABLE
    data_model.change_table(DEFAULT_TABLE)

    # Controller
    table_select.bind('<<ComboboxSelected>>', lambda event, table=selected_table: data_model.change_table(table))

    b1 = tk.Button(scene, text="Ale fajny przycisk")
    b1.pack()

    return scene
