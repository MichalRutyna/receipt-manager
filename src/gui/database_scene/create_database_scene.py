import tkinter as tk

from src.load_config import POSSIBLE_TABLES, DEFAULT_TABLE
from src.internal.data_scene_model import DataModel
from gui.database_scene.data_view import DataView
from gui.database_scene.columnpicker import ColumnPickerView
from gui.database_scene.table_picker import TablePicker


def create_database_scene(parent: tk.Label, database: str) -> tk.Label:
    scene = tk.Label(parent)

    # Model
    data_model = DataModel(database)

    # View
    data_view = DataView(scene, data_model)
    data_model.register_data_view(data_view)

    table_picker = TablePicker(scene, data_model)

    column_picker_view = ColumnPickerView(scene, data_model)
    data_model.register_column_picker(column_picker_view)

    b1 = tk.Button(scene, text="Ale fajny przycisk")
    b1.pack()

    data_model.change_table(DEFAULT_TABLE)

    return scene
