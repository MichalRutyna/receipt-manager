import tkinter as tk
from tkinter import ttk

from src.load_config import POSSIBLE_TABLES, DEFAULT_TABLE
from src.gui.data_view import DataView
from src.gui.columnpicker import ColumnPickerView


def create_database_scene(parent: tk.Label, database: str) -> tk.Label:
    scene = tk.Label(parent)

    selected_table = tk.StringVar()
    table_select = ttk.Combobox(scene, textvariable=selected_table)
    table_select['values'] = POSSIBLE_TABLES
    table_select['state'] = 'readonly'
    table_select.current(POSSIBLE_TABLES.index(DEFAULT_TABLE))
    table_select.pack()

    # View
    data_view = DataView(scene)

    # Model
    from src.internal.database_model import DataModel
    data_model = DataModel(data_view, database)
    data_model.change_table(DEFAULT_TABLE)

    # column picker
    column_picker_view = ColumnPickerView(scene, data_model)
    data_model.register_column_picker(column_picker_view)

    # Controller
    table_select.bind('<<ComboboxSelected>>', lambda event, table=selected_table: data_model.change_table(table))

    b1 = tk.Button(scene, text="Ale fajny przycisk")
    b1.pack()

    return scene
