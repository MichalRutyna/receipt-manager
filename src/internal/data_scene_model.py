from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.database_scene.data_view import DataView
    from gui.database_scene.columnpicker import ColumnPickerView

from src.api.database_to_model import get_table_data

from src.load_config import DEFAULT_DATABASE_COLUMNS, DEFAULT_DATABASE_COLUMN_VALUES


class DataModel:
    def __init__(self, database: str):
        self.view = None
        self.database = database
        self.column_picker = None
        self.table = ""
        self.columns: list[str] = []
        self.column_values: list[bool] = []
        self.rows = []
        self.sorting = {}

    def change_sorting(self, column) -> None:
        """
        Change the sorting of the provided column
        """
        if list(self.sorting.keys()) != [column]:
            self.sorting.clear()
        value = self.sorting.get(column)
        if value is None:
            self.sorting[column] = 'desc'
        elif value == 'desc':
            self.sorting[column] = 'asc'
        else:
            self.sorting.pop(column)

        self.update_views()

    def register_column_picker(self, column_picker: ColumnPickerView) -> None:
        self.column_picker = column_picker

    def register_data_view(self, data_view: DataView) -> None:
        self.view = data_view

    def change_table(self, new_table: tk.StringVar | str) -> None:
        if isinstance(new_table, tk.StringVar):
            new_table = new_table.get()
        if new_table == self.table:
            return
        self.table = new_table
        self.columns = DEFAULT_DATABASE_COLUMNS[new_table]
        self.column_values = DEFAULT_DATABASE_COLUMN_VALUES[new_table]
        self.update_rows()
        self.update_views()

    def change_columns(self, column: str, value: bool) -> None:
        if column in self.columns:
            self.column_values[self.columns.index(column)] = not value
        self.update_rows()
        self.update_views()

    def update_rows(self) -> None:
        show = []
        for i, col in enumerate(self.columns):
            if self.column_values[i]:
                show.append(col)
        if not show:
            return
        self.rows = get_table_data(self.database, self.table, show)

    def update_views(self) -> None:
        if self.view is None:
            return
        show = []
        for i, col in enumerate(self.columns):
            if self.column_values[i]:
                show.append(col)
        if not show:
            # TODO show some alert or sth
            return
        self.view.show(show, self.rows, self.sorting)
        if self.column_picker:
            columns = zip(self.columns, self.column_values)
            self.column_picker.show(list(columns))
