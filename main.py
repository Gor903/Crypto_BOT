import requests
import time
import hmac
import hashlib
import pprint
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY_NEW")
api_secret = os.getenv("SECRET_KEY_NEW")
httpClient=requests.Session()
recv_window=str(5000)
url="https://api.bybit.com" 

def HTTP_Request(endPoint, method, payload, info):
    global time_stamp
    time_stamp=str(int(time.time() * 10 ** 3))
    signature=genSignature(payload)
    headers = {
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-SIGN': signature,
        'X-BAPI-SIGN-TYPE': '2',
        'X-BAPI-TIMESTAMP': time_stamp,
        'X-BAPI-RECV-WINDOW': recv_window,
        'Content-Type': 'application/json'
    }
    if(method=="POST"):
        response = httpClient.request(method, url+endPoint, headers=headers, data=payload)
    else:
        response = httpClient.request(method, url+endPoint+"?"+payload, headers=headers)
    return response.json()

# Hashing keys and creating signatures for Bybit API requests ensures the 
# security and integrity of the requests by verifying their authenticity 
# and preventing tampering or unauthorized access.
def genSignature(payload):
    param_str= str(time_stamp) + api_key + recv_window + payload
    hash = hmac.new(bytes(api_secret, "utf-8"), param_str.encode("utf-8"),hashlib.sha256)
    signature = hash.hexdigest()
    return signature

# This function shows Crypto Coin's prices: Buy and Sell
# Input: 
#     coin - Crypto Coin's short name ("NOT", "DOGE", "BTC")
# Output:
#     {
#        "Buy" : "Ask price",
#        "Sell": "Bid price"
#     }
def get_prices(coin: str) -> dict:
    endpoint="/v5/market/tickers"
    method="GET"
    params=f'category=spot&symbol={coin}USDT'
    response = HTTP_Request(endpoint,method,params,"Ticker")
    return {
        "Buy": response["result"]["list"][0]["ask1Price"],
        "Sell": response["result"]["list"][0]["bid1Price"]
    }

# This functions shows account balance in Bybit.
# Input: 
#     coin - Crypto Coin's short name ("NOT", "DOGE", "BTC")
# Output:
#     {
#        "USD" : "USD amount",
#        "Coin's short name": "Coin amount"
#     }
def get_balance(coin: str="USDT") -> dict:
    endpoint="/v5/account/wallet-balance"
    method="GET"
    params=f'accountType=UNIFIED&coin={coin}'
    response = HTTP_Request(endpoint,method,params,"Balance")
    return {
        "USD": response["result"]["list"][0]["coin"][0]["usdValue"],
        coin: response["result"]["list"][0]["coin"][0]["walletBalance"],
    }

# This function shows min and max order quantity
# Input: 
#     coin - Crypto Coin's short name ("NOT", "DOGE", "BTC")
# Output:
#     {
#        "min" : "min order quantity",
#        "max": "max order quantity"
#     } 
def get_min_order_qty(coin: str) -> dict:
    endpoint="/v5/market/instruments-info"
    method="GET"
    params=f'category=spot&symbol={coin}USDT'
    response = HTTP_Request(endpoint,method,params,"Min qty")
    return {
        "min": response["result"]["list"][0]["lotSizeFilter"]["minOrderQty"],
        "max": response["result"]["list"][0]["lotSizeFilter"]["maxOrderQty"]
    }
    
# Buy or Sell Crypto
# Input: 
#     coin - Crypto Coin's short name ("NOT", "DOGE", "BTC")
#     side - Buy or Sell
#     qty  - Trade quantity, only int value    
# Output:
#     True if order executed successfully
#     False if order executed unsuccessfully
def trade(coin: str, side: str, qty: int) -> bool:
    endpoint="/v5/order/create"
    method="POST"
    params='{"category":"spot","symbol":"'+ coin + 'USDT","side": "' + side + '","orderType":"Market","qty": "' + str(qty) + '","timeInForce":"IOC","isLeverage":0}'
    response = HTTP_Request(endpoint,method,params,"Sell")
    return response["retMsg"] == "OK"


# Contains the primary code to be executed when the script runs directly.
def main():
    # Check internet connection
    if not requests.get("https://www.google.com"):
        return
    print("Code here")
    

# Ensures code runs only when the script is executed directly,
# not when imported as a module
if __name__ == "__main__":
    main()
