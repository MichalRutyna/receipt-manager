import base64
import json
import requests
import pickle

from typing import Dict, Any


class LidlAPI:
    def __init__(self):
        self._access_token = refresh_token()

    def get_access_token(self) -> str:
        # TODO expiration check
        return self._access_token

    def _get_default_headers(self) -> Dict[str, str]:
        return {'Authorization': f'Bearer {self.get_access_token()}',
                'App-Version': '999.99.9',
                'Operating-System': 'ipl',
                'App': 'com.lidl.eci.lidl.plus',
                "Accept-Language": "pl"}

    def _get_coupons(self) -> None:
        # TODO implement coupons
        payload = self._get_default_headers()
        response = requests.get("https://coupons.lidlplus.com/api/v2/PL",
                                headers=payload)
        response = response.json()
        for coupon in response["sections"][1]["coupons"]:
            print(coupon['title'])

    def _get_tickets(self) -> Dict[str, str | int | float | bool | None]:
        """
        Returns a dict representation of a list of tickets
        """
        payload = self._get_default_headers()
        tickets = requests.get("https://tickets.lidlplus.com/api/v2/PL/tickets",
                               headers=payload)

        tickets = tickets.json()

        return tickets

    def _get_ticket(self, ticket_id) -> Dict[str, str | int | float | bool | None]:
        """
        Returns a dict representation of the requested ticket
        """
        payload = self._get_default_headers()
        ticket = requests.get(f"https://tickets.lidlplus.com/api/v2/PL/tickets/{ticket_id}",
                              headers=payload)
        ticket = ticket.json()

        return ticket


def refresh_token() -> str:
    """
    Sends a POST request to the lidl api to refresh the token saved at data/token,
    then saves it to the same file. Returns the access_token
    """
    # TODO encryption
    # TODO checking expiration
    try:
        with open("data/token", 'r') as saved_token:
            lidl_data = json.loads(saved_token.read())
            refresh_token = lidl_data["refresh_token"]
            access_token = lidl_data["access_token"]
    except FileNotFoundError as e:
        print("User token not found. You need to get it from theirs API")
        raise

    CLIENT_ID = "LidlPlusNativeClient"
    secret = base64.b64encode(f"{CLIENT_ID}:secret".encode()).decode()
    response = requests.post("https://accounts.lidl.com/connect/token",
                             headers={'Content-Type': 'application/x-www-form-urlencoded',
                                      'Authorization': f'Basic {secret}'},
                             data={'grant_type': 'refresh_token', "refresh_token": refresh_token})
    response = response.json()

    with open("data/token", mode='w') as token_save_file:
        save_data = str(response).replace("'", "\"")
        token_save_file.write(save_data)

    refresh_token = response["refresh_token"]
    access_token = response["access_token"]

    return access_token


def test_ticket():
    with open("data/test_ticket.pkl", "rb") as f:
        ticket = pickle.load(f)

    print(type(ticket))
    print(ticket)

    from src.database import Database

    with Database("test") as db:
        db.cursor.execute("SELECT * FROM PRAGMA_TABLE_INFO('ticket')")
        print(db.cursor.fetchall())

    id = ticket['id']
    date = ticket['date']
    total = ticket['totalAmountNumeric']
    total_discount = ticket['totalDiscount']

    print(id, date, total, total_discount)


def process_all_tickets(source: LidlAPI) -> None:
    """
    Inserts all tickets into the database
    """
    # TODO Inserting tickets with dates only after last load


def process_ticket(source: LidlAPI, ticket_id: str) -> None:
    """
    Inserts all purchased items from a single ticket into the database
    """


"""
def process_into_database():
    empty_tickets = process_all_tickets()
    for ticket in empty_tickets:
        process_ticket(ticket)
"""
