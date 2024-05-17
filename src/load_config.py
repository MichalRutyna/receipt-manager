TABLES_TRANSLATIONS = {_("categories"): "categories", _("subcategories"): "subcategories",
                       _("products"): "products", _("store_items"): "store_items",
                       _("purchase_instances"): "purchase_instances", _("tickets"): "tickets"}

COLUMNS_TRANSLATIONS = {_('store_item_id') : 'store_item_id',
                        _('store_name'): 'store_name',
                        _('total_amount'): 'total_amount',
                        _('total_spent'): 'total_spent',
                        _('product_id'): 'product_id',
                        _('name'): 'name',
                        }

DEFAULT_TABLE = _('store_items')

POSSIBLE_TABLES = [_("categories"), _("subcategories"),
                   _("products"), _("store_items"),
                   _("purchase_instances"), _("tickets")]

DATABASE_COLUMNS = {
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

DEFAULT_DATABASE_COLUMNS = {
    _('store_items'):
        [
            _('store_name'),
            _('total_amount'),
            _('total_spent'),
            _('name'),
        ],
    _('purchase_instances'):
        [
            _('quantity'),
            _('unit_price'),
            _('discounts'),
            _('store_item_id'),
            _('date'),
        ],
    _('tickets'):
        [
            _('date'),
            _('total'),
            _('total_discount'),
            _('isFavourite'),
        ],
    _('products'):
        [
            _('name'),
            _('subcategory_name'),
            _('isFavourite'),
        ],
    _('categories'):
        [
            _('category_name'),
            _('isFavourite'),
        ],
    _('subcategories'):
        [
            _('subcategory_name'),
            _('isFavourite'),
            _('category_name'),
        ],
}

DEFAULT_DATABASE_COLUMN_VALUES = {
    _('store_items'):
        [
            True, False, True, True
        ],
    _('purchase_instances'):
        [
            True, True, True, True, True
        ],
    _('tickets'):
        [
            True, True, True, True
        ],
    _('products'):
        [
            True, True, True
        ],
    _('categories'):
        [
            True, True
        ],
    _('subcategories'):
        [
            True, True, True
        ],
}