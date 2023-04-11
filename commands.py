import requests
import numpy
exchanges = {
    "Binance": "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
    "Coinbase": "https://api.coinbase.com/v2/prices/BTC-USD/spot",
    "Bitfinex": "https://api.bitfinex.com/v1/pubticker/BTCUSD",
    "Kraken": "https://api.kraken.com/0/public/Ticker?pair=XBTUSD",
    "Bitstamp": "https://www.bitstamp.net/api/v2/ticker/btcusd/"
}

def prices():
    results = []
    for exchange, url in exchanges.items():
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "price" in data:
                price = data["price"]
            elif "last_price" in data:
                price = data["last_price"]
            elif "last" in data:
                price = data["last"]
            result = f'{exchange}  : {price}'
        results.append(result)
    print(results)
    return results
