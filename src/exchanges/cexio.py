import requests
import json
import statistics

PRODUCT_URL = "https://cex.io/api/currency_limits"
BIDS_URL = "https://cex.io/api/order_book/{}/{}?depth={}"


def get_products(filter_str=""):
    """Returns a list of tuples of avaliable products on cex.io exchange"""
    json_get = json.loads(requests.get(PRODUCT_URL).text)
    products = []
    for product in json_get["data"]["pairs"]:
        symbol1 = product["symbol1"]
        symbol2 = product["symbol2"]
        if filter_str == symbol1 or filter_str == symbol2:
            products.append((symbol1, symbol2))

    return products


def average_bid(product1, product2, amount=50):
    """Returns a tuple with the following format (Avg Ask, Avg Bid)"""
    json_bids = json.loads(requests.get(BIDS_URL.format(product1, product2, amount)).text)
    try:
        asks = [float(ask[0]) for ask in json_bids["asks"]]
        bids = [float(bid[0]) for bid in json_bids["bids"]]
    except KeyError:
        print("Wrong product specified. Please use get_products to see avaliable products.")
        return 0
    return statistics.mean(asks), statistics.mean(bids)


#print(average_bid("BTC", "USD", 50))

print(get_products("USD"))
print(average_bid("BTC", "USD", 100))