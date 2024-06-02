import requests
import pprint

main_url = 'https://api.bybit.com/v2/public/tickers'
# main_url = 'https://api.bybit.com/v5/market/tickers'


# GET requests are used to retrieve information from the Bybit API 
# such as market data(coin prices and etc.).
def http_get(url, symbol):
    params = {
         'category': 'inverse',
        'symbol': f'{symbol}USDT',
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to retrieve data: {response.status_code}')

# POST requests are used for executing trading operations,
# such as buying and selling assets.
# These requests require authentication using API key and secret.
# TODO: Start it after finishing GET request method
def http_post():
    pass
    

pprint.pprint(http_get(main_url, "SUPER"))

