import tkinter as tk
from tkinter import ttk

from src.load_config import POSSIBLE_TABLES, DEFAULT_TABLE


class TablePicker:
    def __init__(self, parent, data_model):
        self.model = data_model

        selected_table = tk.StringVar()
        table_select = ttk.Combobox(parent, textvariable=selected_table)

        table_select['values'] = POSSIBLE_TABLES
        table_select['state'] = 'readonly'
        table_select.current(POSSIBLE_TABLES.index(DEFAULT_TABLE))
        table_select.pack()

        table_select.bind('<<ComboboxSelected>>', lambda event, table=selected_table: self.model.change_table(table))
