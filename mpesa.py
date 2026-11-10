import requests
import base64
import math
import models

from datetime import datetime
from requests.auth import HTTPBasicAuth


consumer_key= "RuuPr440Mfe3BwIIoB2D1cTRINlsoKU2dENtQHGdw4PqNAC6"
consumer_secret= "V34pxLrPNdJkr1CAfBeFmFOYjkkGAhYymeUNs3YVXS8uPZ9ZBkqtDqHFtRirXALk"
saf_api_url="https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
saf_short_code="174379"
saf_pass_key="bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
saf_stkpush_api="https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
my_callback_url="https://smartness-reformist-galore.ngrok-free.dev/saf-callback"


def generate_password_and_timestamp():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    password_str = saf_short_code + saf_pass_key + timestamp

    password_bytes = password_str.encode()

    password = base64.b64encode(password_bytes).decode("utf-8")

    return password, timestamp


def get_mpesa_access_token():
    try:
        res = requests.get(
            saf_api_url,
            auth=HTTPBasicAuth(consumer_key, consumer_secret),
        )

        return res.json()['access_token']

    except Exception as e:
        print(str(e), "error getting access token")
        raise e


def make_stk_push(payload):
    amount_paid = payload['amount']
    phone_number = payload['phone_number']
    sale_id = payload.get('sale_id')

    # Dynamically generate token and password on every push
    token = get_mpesa_access_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    password, timestamp = generate_password_and_timestamp()

    push_data = {
        "BusinessShortCode": saf_short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": math.ceil(float(amount_paid)),
        "PartyA": phone_number,
        "PartyB": saf_short_code,
        "PhoneNumber": phone_number,
        "CallBackURL": my_callback_url,
        "AccountReference": str(payload.get('sale_id')),
        "TransactionDesc": "description of the transaction",
    }

    response = requests.post(
        saf_stkpush_api,
        json=push_data,
        headers=headers
    )

    return response.json()

    