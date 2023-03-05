import pydantic
import datetime


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
    store: str
    date: datetime.date
