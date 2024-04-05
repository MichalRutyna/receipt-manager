from api import LidlAPI
from store_database import StoreDatabase
from typing import Iterable, List
import sqlite3
import json


def process_ticket_page(source: LidlAPI, target: str, page: int) -> Iterable[str]:
    """
    Inserts all tickets into the database
    Target is the name of the target database
    Returns an iterable of ids of empty tickets - tickets that have no items
    """
    # TODO Inserting tickets with dates only after last load
    # TODO check if all receipts are loaded (if oldest_loaded_ticket['date'] > newest_ticket_database['date'])
    ticket_list: dict = source.get_tickets(page=page)
    ticket_list: List[dict] = ticket_list['tickets']

    with StoreDatabase(target) as db:
        db.cursor.execute("BEGIN TRANSACTION")
        for ticket in ticket_list:
            ticket_id: int = int(ticket['id'])
            date: str = str(ticket['date'])
            total: float = float(ticket['totalAmount'])
            fav = 1 if ticket['isFavorite'] else 0
            print(ticket_id, repr(date), total, fav)
            try:
                db.cursor.execute("INSERT INTO tickets (store_id, date, total, total_discount, isFavourite) "
                                  f"VALUES ('{ticket_id}', '{date}', {total}, 0, {fav})")
            except sqlite3.IntegrityError as e:
                print(e)
        db.cursor.execute("SELECT * from tickets")
        print(db.cursor.fetchall())
        db.cursor.execute("COMMIT TRANSACTION")


def process_ticket(source: LidlAPI, target, ticket_id: str) -> None:
    """
    Inserts all purchased items from a single ticket into the database
    """
    with StoreDatabase(target) as db:
        db.cursor.execute("BEGIN TRANSACTION")
        try:
            db.cursor.execute("INSERT INTO tickets (date, total, total_discount, isFavourite) "
                              "VALUES ('2024-04-03T14:41:48+00:00', 92.05, 0, FALSE)")
        except sqlite3.IntegrityError as e:
            print("Duplicate value")
        db.cursor.execute("COMMIT TRANSACTION")
        db.cursor.execute("SELECT * FROM tickets")
        print(db.cursor.fetchall())


def update_into_database(source: LidlAPI, target) -> None:
    """
    Updates the database with new tickets and items
    """
    empty_tickets = process_ticket_page(source, target, 1)
    # for ticket in empty_tickets:
    #     process_ticket(source, target, ticket)


def fill_empty_database(source: LidlAPI, target) -> None:
    pass
