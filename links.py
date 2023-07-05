import requests
import time
import datetime
import sys
exchanges = {
'Binance' : 'https://api.binance.com/api/v3/depth?symbol=BTCUSDT&limit=1000',
'CoinBase' : 'https://api.pro.coinbase.com/products/BTC-USD/book?level=2',
'Bitfinex' : 'https://api-pub.bitfinex.com/v2/book/tBTCUSD/P0?len=100',
'Gate.io' :' https://data.gateapi.io/api2/1/orderBook/btc_usdt ',
'BitStamp' :'https://www.bitstamp.net/api/v2/order_book/btcusd/',
'OKX' : ' https://www.okex.com/api/v5/market/books?instId=BTC-USDT&sz=5',
'Kraken' : 'https://api.kraken.com/0/public/Depth?pair=XBTUSD&count=100',
'bitFlyer' : 'https://api.bitflyer.com/v1/getboard?product_code=BTC_USD',
'Huobi' : 'https://api.huobi.pro/market/depth?symbol=btcusdt&type=step0',
'Bitrue' :'https://www.bitrue.com/api/v1/depth?symbol=BTCUSDT&limit=50',
'Bybit' : 'https://api.bybit.com/v2/public/orderBook/L2?symbol=BTCUSD',
'Gemini' : 'https://api.gemini.com/v1/book/btcusd?limit_bids=100&limit_asks=100',
'Coincheck' : 'https://coincheck.com/api/order_books?pair=btc_jpy&depth=5',
'Lbank' :'https://api.lbkex.com/v2/depth.do?symbol=btc_usdt&size=50',
'Coinsbit' : 'https://coinsbit.io/api/v1/public/orderbook/BTC_USDT',
'EXMO' : 'https://api.exmo.com/v1/order_book/?pair=BTC_USDT',
'itBit' :'https://api.itbit.com/v1/markets/XBTUSD/order_book',
'Upbit' :'https://api.upbit.com/v1/orderbook?markets=USDT-BTC',
#'Dcoin' : 'https://openapi.dcoin.com/open/api/market_dept?symbol=btc_usdt&type=step0&size=10',
#'XT.COM' : ' https://www.xt.com/api/depth?symbol=btcusdt&size=5 ',
#'BTCEX' : ' https://www.btcex.com/api/v1/depth?symbol=btc_usdt&limit=50 ',
#'Tidex' : ' https://api.tidex.com/api/3/depth/btc_usdt?limit=20 ',
#'CoinZoom' : ' https://tradeapi.coinzoom.com/orderbook?symbol=BTC_USD&limit=10 ',
#'Pionex' :'https://api.pionex.com/trade-api/market/orderbook?symbol=BTCUSDT&depth=5',
#'P2B' : ' https://p2b-exchange.com/api/public/v1/orderbook?market=BTC/USDT&depth=5',
#'WhiteBit': 'https://whitebit.com/api/v4/public/orderbook?market=BTC_USD&limit=5',
#'CoinTRPro' : 'https://api.cointr.pro/v1/market/orderbook?symbol=BTC/USDT&depth=5',
#'Crypto.com_Exchanges' : ' https://api.crypto.com/v2/public/order_book?instrument_name=BTC_USDT&depth=5',
#'BKEX' : 'https://api.bkex.com/v1/q/ticker?symbol=btc_usdt&depth=5',
#'WOO_X' : 'https://api.woo.network/v1/order-book/BTC-USD',
#'DigiFinex' :' https://openapi.digifinex.com/v2/order_book?symbol=btc_usdt',
#'GMO Japan' : ' https://api.coin.z.com/public/v1/orderbooks/BTC/JPY',
#'C-Patex' : ' https://c-patex.com/api/v1/public/getorderbook?market=btc_usdt',
#'BTSE' : ' https://api.btse.com/spot/api/v3.2/orderbook/L2?symbol=BTCPFC&group=1',
#'BitMart' : 'https://api-cloud.bitmart.com/spot/v1/depth?symbol=BTC_USDT&precision=1',
#'Dex-Trade' : 'https://dex-trade.com/api/v1/orderbook/btc_usd',
#'Bitbank' : ' https://public.bitbank.cc/btc_jpy/depth ',
#'OKX' : 'https://www.okex.com/api/spot/v3/instruments/BTC-USDT/book?size=100',
#'BingX' : 'https://www.bingx.com/api/v1/swap/market/depth?contract=BTC-USDT&type=step0',
#'LATOKEN' : 'https://api.latoken.com/v2/order-book/BTC-USDT',
#'PointPay':'https://api.pointpay.io/api/v2/depth?market=btc_usdt',
#'Bitvavo' :'https://api.bitvavo.com/v2/book?market=BTC-EUR',
#'BigOne' :'https://openapi.big.one/api/v3/depth?symbol=btc-usdt&limit=50'
#'Cryptology':'https://api.cryptology.com/v1/markets/BTC_USDT/order-book?limit=10',
#'FinexBox':'https://api.finexbox.com/v1/market/orderbook?market=btc_usdt',
#'KuCoin':'https://api.kucoin.com/api/v1/market/orderbook/level2_100?symbol=BTC-USDT',
#'Txbit':'https://api.txbit.io/api/v2/orderbook?market=btc_usd&type=both',
}

results = []
for exchange, url in exchanges.items():
    response = requests.get(url)
    data = response.json()
    result = f'{exchange}  : {data} \n =======================\n {exchange}'
    #print(result)
    if "bids" in data:
        bids = data["bids"]
        print(f'{exchange}:\nBIDS{bids} \n BIDS{exchange}')
    if "asks" in data:
        asks = data["asks"]
        print(f'{exchange}:\nASKS{asks} \n ASKS{exchange}')
        print(asks)


