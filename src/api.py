import base64
import json
import requests
import pickle

from typing import Any


class LidlAPI:
    def __init__(self):
        self._access_token = refresh_token()

    def get_access_token(self) -> str:
        # TODO expiration check
        return self._access_token

    def _get_default_headers(self) -> dict[str, str]:
        return {'Authorization': f'Bearer {self.get_access_token()}',
                'App-Version': '999.99.9',
                'Operating-System': 'ipl',
                'App': 'com.lidl.eci.lidl.plus',
                "Accept-Language": "pl"}

    def get_coupons(self) -> None:
        # TODO implement coupons
        payload = self._get_default_headers()
        response = requests.get("https://coupons.lidlplus.com/api/v2/PL",
                                headers=payload)
        response = response.json()
        for coupon in response["sections"][1]["coupons"]:
            print(coupon['title'])

    def get_tickets(self, page) -> dict[str, str | int | float | bool | list[dict] | None]:
        """
        Returns a dict representation of a list of tickets
        """
        payload = self._get_default_headers()
        tickets = requests.get(f"https://tickets.lidlplus.com/api/v2/PL/tickets?pageNumber={page}",
                               headers=payload)

        tickets = tickets.json()

        return tickets

    def get_ticket(self, ticket_id) -> dict[str, str | int | float | bool | list[dict] | None]:
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
            refresh_token_part = lidl_data["refresh_token"]
            access_token = lidl_data["access_token"]
    except FileNotFoundError as e:
        # TODO user token creation
        print("User token not found. You need to get it from theirs API")
        raise

    CLIENT_ID = "LidlPlusNativeClient"
    secret = base64.b64encode(f"{CLIENT_ID}:secret".encode()).decode()
    response = requests.post("https://accounts.lidl.com/connect/token",
                             headers={'Content-Type': 'application/x-www-form-urlencoded',
                                      'Authorization': f'Basic {secret}'},
                             data={'grant_type': 'refresh_token', "refresh_token": refresh_token_part})
    response = response.json()

    with open("data/token", mode='w') as token_save_file:
        save_data = str(response).replace("'", "\"")
        token_save_file.write(save_data)

    refresh_token_part = response["refresh_token"]
    access_token = response["access_token"]

    return access_token


def test_ticket():
    #with open("data/test_ticket.pkl", "rb") as f:
    #    ticket = pickle.load(f)

    from src.store_database import StoreDatabase

    with StoreDatabase("test") as db:
        db.cursor.execute("SELECT * FROM PRAGMA_TABLE_LIST()")
        print(db.cursor.fetchall())


