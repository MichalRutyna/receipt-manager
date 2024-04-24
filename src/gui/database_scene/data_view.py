from __future__ import annotations

from tkinter import ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from internal.data_scene_model import DataModel


class DataView:
    def __init__(self, parent, data_model: DataModel):
        self.parent = parent
        self.model = data_model

        self.tree = ttk.Treeview(self.parent, show='headings', selectmode='none', height=25)
        self.tree.bind("<Button-1>", self.on_double_click)
        self.tree.pack()

    def on_double_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "heading":
            column = self.tree.identify_column(event.x)
            column = self.tree.column(column, 'id')
            self.model.change_sorting(column)

    def show(self, columns: list[str], data: list[list[any]]) -> None:
        """
        Send the appropriate data to the GUI
        """
        # delete all data being shown
        self.tree['columns'] = columns
        self.tree.delete(*self.tree.get_children())
        for i in range(1, len(columns) + 1):
            self.tree.heading(f"#{i}", text=columns[i - 1])

        for row in data:
            self.tree.insert('', 'end', values=row)
