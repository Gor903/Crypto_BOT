import requests
import pprint

main_url = 'https://api.bybit.com/v2/public/tickers'
# main_url = 'https://api.bybit.com/v5/market/tickers'


# GET requests are used to retrieve information from the Bybit API 
# such as market data(coin prices and etc.).
def http_get(url, params=None):
    try:
        response = requests.get(url, params=params)
    except Exception as e:
        return print(e)

    if response.status_code == 200:
        return response
    else:
        return False

# POST requests are used for executing trading operations,
# such as buying and selling assets.
# These requests require authentication using API key and secret.
# TODO: Start it after finishing GET request method
def http_post():
    pass
    
# Contains the primary code to be executed when the script runs directly.
def main():
    # Check internet connection
    if not http_get("https://www.google.com"):
        return
    
    # Example
    params = {
        'category': 'inverse',
        'symbol': 'BTCUSDT',
    }
    response = http_get(main_url, params)
    pprint.pprint(response.json())


# Ensures code runs only when the script is executed directly,
# not when imported as a module
if __name__ == "__main__":
    main()
