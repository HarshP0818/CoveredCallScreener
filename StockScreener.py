# Find all stock that are US equities and have a price less than $100
import json

from alpaca.trading import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass
import keys
import requests


trading_client = TradingClient(keys.alpaca_api_key, keys.alpaca_api_secret_key, paper=True)

search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)

assets = trading_client.get_all_assets(search_params)

headers = {
    "accept": "application/json",
    "APCA-API-KEY-ID": keys.alpaca_api_key,
    "APCA-API-SECRET-KEY": keys.alpaca_api_secret_key
    }

min_price = 10.00
max_price = 100.00

# FILTERING STOCKS WITHIN A CERTAIN PRICE RANGE
#######################################################################################################################
filtered_stock = []

max_count = 0
for asset in assets:
    if max_count < 5:
        max_count = len(filtered_stock)
        if asset.tradable:
            url = f"https://data.alpaca.markets/v2/stocks/quotes/latest?symbols={asset.symbol}&feed=iex"
            response = requests.get(url, headers=headers)
            data = json.loads(response.text)
            symbol = asset.symbol
            if 'quotes' in data:
                if symbol in data['quotes']:
                    price = data['quotes'][symbol]['ap']
                    if min_price < price < max_price:
                        filtered_stock.append((symbol, price))
    else:
        break
#######################################################################################################################

# It might be easier to filter by market cap or using another API to filter stocks and then use Alpaca to trade
