import tkinter as tk

from src.gui.data_view import DataView
from src.gui.columnpicker import ColumnPickerView
from src.api.database_to_model import get_table_data

from src.load_config import DATABASE_COLUMNS


class DataModel:
    def __init__(self, view: DataView, database: str):
        self.view = view
        self.database = database
        self.column_picker = None
        self.table = ""
        self.columns = []
        self.column_values = []
        self.rows = []

    def register_column_picker(self, column_picker: ColumnPickerView):
        self.column_picker = column_picker

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
        self.view.show(self.columns, self.rows)
        if self.column_picker:
            self.column_picker.show(self.columns, self.column_values)
