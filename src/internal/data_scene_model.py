from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.database_scene.data_view import DataView
    from gui.database_scene.columnpicker import ColumnPickerView

from src.api.database_to_model import get_table_data

from src.load_config import DATABASE_COLUMNS


class DataModel:
    def __init__(self, database: str):
        self.view = None
        self.database = database
        self.column_picker = None
        self.table = ""
        self.columns = []
        self.column_values = []
        self.rows = []
        self.sorting = {}

    def change_sorting(self, column):
        """
        Change the sorting of the provided column
        """
        value = self.sorting.get(column)
        if value is None:
            self.sorting[column] = 'desc'
        elif value == 'desc':
            self.sorting[column] = 'asc'
        else:
            self.sorting.pop(column)

        print(self.sorting)

    def register_column_picker(self, column_picker: ColumnPickerView):
        self.column_picker = column_picker

    def register_data_view(self, data_view: DataView):
        self.view = data_view

    def change_table(self, new_table: tk.StringVar | str) -> None:
        if isinstance(new_table, tk.StringVar):
            new_table = new_table.get()
        if new_table == self.table:
            return
        self.table = new_table
        self.columns = DATABASE_COLUMNS[new_table]
        self.column_values = None  # TODO default columns to show
        self.update_rows()
        self.update_views()

    def change_columns(self, column: str, value: bool) -> None:
        if value and column not in self.columns:
            self.columns.append(column)
        elif not value and column in self.columns:
            self.columns.remove(column)
        self.update_views()

    def update_rows(self) -> None:
        self.rows = get_table_data(self.database, self.table)

    def update_views(self) -> None:
        if self.view is None:
            return
        self.view.show(self.columns, self.rows)
        if self.column_picker:
            self.column_picker.show(self.columns, self.column_values)
