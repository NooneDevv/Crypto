import requests
import json
import statistics

PRODUCT_URL = "https://api.binance.com/api/v3/ticker/price"
BIDS_URL = "https://api.binance.com/api/v1/depth?symbol={}&limit={}"
#TRADE HISTORY https://api.binance.com/api/v1/trades?symbol=BTCUSDT&limit=5


def get_products(filter_str=""):
    """Returns a list of tuples of avaliable products on binance exchange"""
    json_get = json.loads(requests.get(PRODUCT_URL).text)
    products = []
    for product in json_get:
        symbol = product["symbol"]
        if filter_str in symbol:
            products.append(symbol)

    return products


def average_bid(product, amount=50):
    """Returns a tuple with the following format (Avg Ask, Avg Bid)"""
    json_bids = json.loads(requests.get(BIDS_URL.format(product, amount)).text)
    try:
        asks = [float(ask[0]) for ask in json_bids["asks"]]
        bids = [float(bid[0]) for bid in json_bids["bids"]]
    except KeyError:
        print("Wrong product specified. Please use get_products to see avaliable products.")
        return 0
    return statistics.mean(asks), statistics.mean(bids)
