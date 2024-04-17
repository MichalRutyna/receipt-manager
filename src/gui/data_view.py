import tkinter as tk
from tkinter import ttk

DATABASE_TABLES = {
    _('store_items'):
        [
            _('store_item_id'),
            _('store_name'),
            _('total_amount'),
            _('total_spent'),
            _('product_id'),
        ],
    _('purchase_instances'):
        [
            _('instance_id'),
            _('quantity'),
            _('unit_price'),
            _('discounts'),
            _('store_item_id'),
            _('ticket_id'),
        ],
    _('tickets'):
        [
            _('ticket_id'),
            _('date'),
            _('total'),
            _('total_discount'),
            _('isFavourite'),
        ],
    _('products'):
        [
            _('product_id'),
            _('name'),
            _('subcategory_id'),
            _('isFavourite'),
        ],
    _('categories'):
        [
            _('category_id'),
            _('category_name'),
            _('isFavourite'),
        ],
    _('subcategories'):
        [
            _('subcategory_id'),
            _('subcategory_name'),
            _('isFavourite'),
            _('category_id'),
        ],
}

POSSIBLE_TABLES = [_("categories"), _("subcategories"),
                   _("products"), _("store_items"),
                   _("purchase_instances"), _("tickets")]

DEFAULT_TABLE = _('store_items')


class DataView:
    def __init__(self, parent):
        self.parent = parent
        self.table = []
        self.columns = []
        self.length = 0

        self.tree = ttk.Treeview(self.parent, show='headings')
        self.tree.pack()

        self.change_table(DEFAULT_TABLE)

    def show(self) -> None:
        """
        Send the appropriate data to the GUI
        """
        # delete all data being shown
        self.tree['columns'] = self.columns
        self.tree.delete(*self.tree.get_children())
        for i in range(1, self.length + 1):
            self.tree.heading(f"#{i}", text=self.columns[i - 1])
            
        #get_data()

    def add_column(self):
        pass

    def change_table(self, new_table: tk.StringVar | str) -> None:
        if isinstance(new_table, tk.StringVar):
            new_table = new_table.get()
        self.table = new_table
        self.columns = DATABASE_TABLES[new_table]
        self.length = len(self.columns)
        self.show()


def create_database_scene(parent) -> tk.Label:
    print(_("Witaj world"))
    scene = tk.Label(parent)

    selected_table = tk.StringVar()
    table_select = ttk.Combobox(scene, textvariable=selected_table)
    table_select['values'] = POSSIBLE_TABLES
    table_select['state'] = 'readonly'
    table_select.pack()

    data_view = DataView(scene)

    table_select.bind('<<ComboboxSelected>>', lambda event, table=selected_table: data_view.change_table(table))

    b1 = tk.Button(scene, text="Ale fajny przycisk")
    b1.pack()

    return scene
