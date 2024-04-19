from tkinter import ttk


class DataView:
    def __init__(self, parent):
        self.parent = parent

        self.tree = ttk.Treeview(self.parent, show='headings')
        self.tree.pack()

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
