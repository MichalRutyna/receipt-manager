import pydantic
import datetime
import logging


class Item(pydantic.BaseModel):
    """
    Represents items known

    Item(name: str,
        median_price: float,

        category: str)
    """
    name: str
    mean_price: float
    category: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logging.debug(f"Created Item object {self.name}. Mean price: {self.mean_price}, category: {self.category}")


class Purchase(pydantic.BaseModel):
    """
    Represents individual purchase

    Purchase(item: Item,
        price: float,

        store: str,

        date: datetime.date)
    """
    item: Item
    price: float
    amount: int
    store: str
    date: datetime.date

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logging.debug(f"Created Purchase object ({self.item}). Price: {self.price}, Amount: {self.amount} store: {self.store}, date: {self.date}")
