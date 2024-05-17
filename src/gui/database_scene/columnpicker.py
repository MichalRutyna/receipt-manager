import tkinter as tk
from tkinter import ttk


class ColumnPickerView:
    def __init__(self, scene, data_model):
        self.column_pickers = []
        self.picker_variables = []
        self.shown_columns = []
        self.parent = scene
        self.data_model = data_model

    def show(self, columns: list[tuple[str, bool]]):
        if columns != self.shown_columns:
            print(self.column_pickers)
            for picker in self.column_pickers:
                picker.pack_forget()
                del picker
            self.column_pickers = []
            self.picker_variables = []
            for column in columns:
                variable = tk.IntVar()
                variable.set(column[1])
                self.picker_variables.append(variable)
                self.column_pickers.append(
                    ttk.Checkbutton(self.parent, text=column[0],
                                    variable=variable,
                                    command=lambda x=column[0], value=variable.get():
                                        self.data_model.change_columns(x, bool(value)))
                )
                print(self.column_pickers)
                self.column_pickers[-1].pack()
