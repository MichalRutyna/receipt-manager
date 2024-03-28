import base64
import json
import requests


def test_api():
    import json
    import string

    CLIENT_ID = "LidlPlusNativeClient"

    try:
        with open("data/token2", mode='r') as token_save_file:
            lidl_data = json.loads(token_save_file.read())
            _refresh_token = lidl_data["refresh_token"]
            _access_token = lidl_data["access_token"]
    except Exception as e:
        with open("data/token", mode='r') as token_backup:
            lidl_data = json.loads(token_backup.read())
            _refresh_token = lidl_data["refresh_token"]
            _access_token = lidl_data["access_token"]
        print(e)

    secret = base64.b64encode(f"{CLIENT_ID}:secret".encode()).decode()
    response = requests.post("https://accounts.lidl.com/connect/token",
                             headers={'Content-Type': 'application/x-www-form-urlencoded',
                                      'Authorization': f'Basic {secret}'},
                             data={'grant_type': 'refresh_token', "refresh_token": _refresh_token}).json()
    # print(response)

    with open("data/token2", mode='w') as token_save_file:
        save_data = str(response).replace("'", "\"")
        token_save_file.write(save_data)

    _refresh_token = response["refresh_token"]
    _access_token = response["access_token"]
    payload = _get_default_headers(_access_token)
    _get_ticket(payload, 2400153482202403222240)


def _get_default_headers(token):
    return {'Authorization': f'Bearer {token}',
            'App-Version': '999.99.9',
            'Operating-System': 'ipl',
            'App': 'com.lidl.eci.lidl.plus',
            "Accept-Language": "pl"}


def _get_coupons(load):
    response = requests.get("https://coupons.lidlplus.com/api/v2/PL", headers=load).json()
    for coupon in response["sections"][1]["coupons"]:
        print(coupon['title'])


def _get_tickets(load):
    tickets = requests.get("https://tickets.lidlplus.com/api/v2/PL/tickets", headers=load).json()
    print(str(tickets).replace("'", "\""))


def _get_ticket(load, ticket_id):
    ticket = requests.get(f"https://tickets.lidlplus.com/api/v2/PL/tickets/{ticket_id}", headers=load)
    print(ticket.text)
    with open("data/test_ticket", "w", encoding="utf-8") as file:
        file.write(str(ticket.json()).replace("'", "\""))
    try:
        print(str(ticket.json()).replace("'", "\""))
    except Exception as e:
        print(e)


def test_ticket():
    with open("data/test_ticket", "r", encoding="utf-8") as file:
        saved_ticket = file.read()
    ticket = json.dumps(saved_ticket)
    print(type(ticket))
    print(ticket)
