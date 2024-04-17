import logging

from api.main_api import LidlAPI
from store_database import StoreDatabase
from typing import Iterable, List
import sqlite3
import json


def process_ticket_page(source: LidlAPI, target: str, page: int, force_ticket_processing: bool = False)\
        -> Iterable[str] | None:
    """
    Inserts all tickets into the database
    Target is the name of the target database
    force_ticket_processing forces all tickets on the provided page to be put through item processing
    Returns an iterable of ids of processed tickets
    Returns None if the page was empty
    """
    # TODO Inserting tickets with dates only after last load
    # TODO check if all receipts are loaded (if oldest_loaded_ticket['date'] > newest_ticket_database['date'])
    print(f"Processing ticket page {page}")
    ticket_list: dict = source.get_ticket_page(page=page)
    ticket_list: List[dict] = ticket_list['tickets']
    empty_tickets: List[str] = []

    if len(ticket_list) == 0:
        logging.warning('Process ticket page called with an empty page')
        return None

    with StoreDatabase(target) as db:
        db.cursor.execute("BEGIN TRANSACTION")
        for ticket in ticket_list:
            ticket_id: str = str(ticket['id'])
            date: str = str(ticket['date'])
            total: float = float(ticket['totalAmount'])
            fav = 1 if ticket['isFavorite'] else 0

            try:
                db.cursor.execute(f"SELECT 1 FROM tickets WHERE ticket_id = ?", [ticket_id])
                # Only process new a ticket if it doesn't exist already
                if db.cursor.fetchone() is None:
                    db.cursor.execute("INSERT INTO tickets (ticket_id, date, total, total_discount, isFavourite) "
                                      f"VALUES (?, ?, ?, 0, ?)", [ticket_id, date, total, fav])
                    empty_tickets.append(f'{ticket_id}')
                elif force_ticket_processing:
                    empty_tickets.append(f'{ticket_id}')
            except sqlite3.IntegrityError as e:
                logging.error("IntegrityError occurred during creation of a new ticket")
                logging.error(e)

        db.cursor.execute("COMMIT TRANSACTION")

    for empty_ticket in empty_tickets:
        process_ticket(source, target, empty_ticket)
    return empty_tickets


def process_ticket(source: LidlAPI, target: str, ticket_id: str) -> None:
    """
    Inserts all purchased items from a single ticket into the database
    Target is the name of the target database
    """
    print(f"Processing ticket {ticket_id}")
    ticket = source.get_ticket(ticket_id)

    with StoreDatabase(target) as db:
        db.cursor.execute("BEGIN TRANSACTION")

        for item in ticket['itemsLine']:
            # creating a store_item if it doesn't already exist
            try:
                code_input: str = str(item['codeInput'])
                name: str = str(item['name'])

                db.cursor.execute(f"SELECT 1 FROM store_items WHERE store_item_id = ?", [code_input])
                # Only create new store_item if it doesn't exist already
                if db.cursor.fetchone() is None:
                    db.cursor.execute("INSERT INTO store_items (store_item_id, store_name) "
                                      "VALUES (?, ?)", [code_input, name])
                    logging.log(logging.INFO, f'Created new store item: {name}')
            except sqlite3.IntegrityError as e:
                logging.error("IntegrityError occurred during creation of a new store_item")
                logging.error(e)
            except Exception as e:
                logging.error(e)
                logging.error("Error occured during execution of INSERT INTO store_items (store_item_id, store_name) "
                              f"VALUES (?, ?)", [code_input, name])
                raise

            # inserting purchase instance
            try:
                discount_amount = 0.0
                for discount in item['discounts']:
                    discount_amount += float(discount['amount'].replace(',', '.'))
                store_item_id = item['codeInput']
                unit_price = float(item['currentUnitPrice'].replace(',', '.'))
                quantity = float(item['quantity'].replace(',', '.'))

                db.cursor.execute(
                    f"INSERT INTO purchase_instances (quantity, unit_price, discounts, ticket_id, store_item_id) "
                    f"VALUES (?, ?, ?, ?, ?)",
                    [quantity, unit_price, discount_amount, ticket_id, store_item_id]
                )

                db.cursor.execute(
                    f"UPDATE store_items SET total_amount = total_amount + {quantity},"
                    f" total_spent = total_spent + round({quantity * unit_price}, 2) WHERE store_item_id=?",
                    [store_item_id]
                )

                db.cursor.execute(
                    f"UPDATE tickets SET total_discount = total_discount + {discount_amount} WHERE ticket_id=?",
                    [ticket_id]
                )

                db.cursor.execute("SELECT MAX(instance_id) FROM purchase_instances")
                logging.log(logging.INFO, f'Created new purchase instance: {name}, id = {db.cursor.fetchone()}')

            except sqlite3.IntegrityError as e:
                logging.error(e)
                logging.error(f"The above error was encounter during inserting a purchase instance: {store_item_id},"
                              f" in the ticket {ticket_id}")

        db.cursor.execute("COMMIT TRANSACTION")


def update_into_database(source: LidlAPI, target) -> None:
    """
    Updates the database with new tickets and items
    """
    # TODO only update new stuff
    process_ticket_page(source, target, 1)


def fill_missing_data(source: LidlAPI, target) -> None:
    """
    Does a full swipe of the database and updates all the missing data
    """

    # updating missing tickets
    fail = False
    page = 10
    while not fail:
        try:
            processed_tickets = process_ticket_page(source, target, page, True)
            if processed_tickets is None:
                fail = True
            page += 1

        except sqlite3.IntegrityError as e:
            logging.error(e)

    # store items sums recalculation
    with StoreDatabase(target) as db:
        db.cursor.execute("BEGIN TRANSACTION")

        db.cursor.execute("SELECT quantity, unit_price, store_item_id from purchase_instances")
        instances = db.cursor.fetchall()

        # clear old totals
        try:
            db.cursor.execute(f"UPDATE store_items SET total_amount = 0, total_spent = 0")
        except sqlite3.IntegrityError as e:
            db.cursor.execute("ROLLBACK")
            logging.error(e)
            return

        for instance in instances:
            quantity, unit_price, store_item_id = instance
            try:
                db.cursor.execute(
                    f"UPDATE store_items SET total_amount = total_amount + ?,"
                    f" total_spent = total_spent + round(?, 2) WHERE store_item_id=?",
                    [quantity, quantity * unit_price, store_item_id]
                )
            except sqlite3.IntegrityError as e:
                logging.error(e)

        db.cursor.execute("COMMIT TRANSACTION")
