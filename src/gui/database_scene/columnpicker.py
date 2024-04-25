import tkinter as tk
from tkinter import ttk


class ColumnPickerView:
    def __init__(self, scene, data_model):
        self.column_pickers = []
        a = ttk.Button(scene, text="Test picker", command=lambda b="asda": data_model.change_columns(b, True))
        a.pack()

    def show(self, columns, column_values):
        print("picker")
