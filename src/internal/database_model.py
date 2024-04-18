import tkinter as tk

from src.gui.data_view import DataView
from src.api.database_to_model import *

# TODO Config
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


class DataModel:
    def __init__(self, view: DataView):
        self.view = view
        self.table = ""
        self.columns = []
        self.data = []

    def change_table(self, new_table: tk.StringVar | str) -> None:
        if isinstance(new_table, tk.StringVar):
            new_table = new_table.get()
        self.table = new_table
        self.columns = DATABASE_TABLES[new_table]
        self.update_view()

    def update_data(self) -> None:
        pass

    def update_view(self) -> None:
        self.view.show(self.columns, self.data)
