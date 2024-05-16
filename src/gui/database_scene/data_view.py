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
        self.tree.bind("<Button-1>", self.on_click)
        self.tree.pack()

    def on_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "heading":
            column = self.tree.identify_column(event.x)
            column = self.tree.column(column, 'id')
            self.model.change_sorting(column)

    def show(self, columns: list[str], data: list[list[any]], sorting: dict[str, str]) -> None:
        """
        Send the appropriate data to the GUI
        """
        # delete all data being shown
        temp = []
        for row in data:
            row = list(row)
            row = [x if x is not None else "Not set" for x in row]
            temp.append(row)
        data = temp

        columns_text = columns.copy()
        if len(sorting) > 1:
            raise ValueError("There was more than one column to be sorted by")
        if len(sorting) == 1:
            sorting = tuple(sorting.items())[0]
            if sorting[1] == 'asc':
                val = "↑"
                reverse = False
            elif sorting[1] == 'desc':
                val = "↓"
                reverse = True
            else:
                raise ValueError("Sorting supplied with wrong value")
            columns_text[columns.index(sorting[0])] += val

            data.sort(key=lambda x: x[columns.index(sorting[0])], reverse=reverse)

        self.tree['columns'] = columns
        self.tree.delete(*self.tree.get_children())
        for i in range(1, len(columns) + 1):
            self.tree.heading(f"#{i}", text=columns_text[i - 1])

        for row in data:
            self.tree.insert('', 'end', values=row)
