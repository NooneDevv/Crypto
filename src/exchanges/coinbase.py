import requests
import json
import statistics

PRODUCT_URL = "https://api.pro.coinbase.com/products"
BIDS_URL = "https://api.pro.coinbase.com/products/{}/book?level={}"


def get_products(filter_str=""):
    """Returns avaliable products at coinbase, use filter_str to filter"""
    json_get = json.loads(requests.get(PRODUCT_URL).text)
    products = []
    for product in json_get:
        identifier = product["id"]
        if filter_str in identifier:
            products.append(identifier)

    return products


def average_bid(product, level=2):
    """Returns a tuple with the following format (Avg Ask, Avg Bid)"""
    """Level 1 = 1 bid/ask, Level 2 - 50 bids/asks, Level 3 - ALL Bids/Asks [Avoid usage]"""
    json_bids = json.loads(requests.get(BIDS_URL.format(product, level)).text)
    try:
        asks = [float(ask[0]) for ask in json_bids["asks"]]
        bids = [float(bid[0]) for bid in json_bids["bids"]]
    except KeyError:
        print("Wrong product specified. Please use get_products to see avaliable products.")
        return 0
    return statistics.mean(asks), statistics.mean(bids)


print(average_bid("BTC-USD"))
print(get_products("USD"))
