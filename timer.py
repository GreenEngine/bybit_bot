import requests
import time
global upflag
global dawnflag

def prices():
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
            print(exchange, ":", price)
    #print(comp)

    #как расчитать к
exchanges = {
    "Binance": "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
    "Coinbase": "https://api.coinbase.com/v2/prices/BTC-USD/spot",
    "Bitfinex": "https://api.bitfinex.com/v1/pubticker/BTCUSD",
    "Kraken": "https://api.kraken.com/0/public/Ticker?pair=XBTUSD",
    "Bitstamp": "https://www.bitstamp.net/api/v2/ticker/btcusd/"
}
complited_orders = 'https://api.bybit.com/v2/public/execution/list?symbol=BTCUSD&limit=50&order_status=Filled'
upflag = 0
dawnflag = 0
#upflag[10] = {0,0,0,0,0,0,0,0,0,0}
#dawnflag[10] = {0,0,0,0,0,0,0,0,0,0}
while(1):

    url = f'https://api.bybit.com/v2/public/orderBook/L2?category=spot&symbol=BTCUSD&depth=50&price=BTC'
    response = requests.get(url)
    data = response.json()
    buy_data = []
    sell_data = []
    buy_total = 0
    sell_total = 0
    buy_total_size = 0
    sell_total_size = 0
    complited = 'https://api.bybit.com/v2/public/execution/list?symbol=BTCUSD&limit=50&order_status=Filled'
    resp= requests.get(complited)
    comp = response.json()
    ur = f'https://api.bybit.com/v2/public/tickers?symbol=BTCUSD'
    response = requests.get(ur)
    price = response.json()['result'][0]['last_price']
    #счита сколько в долларах капитализация вычитаем или прибавляем
    for item in comp['result']:
        price = item['price']
        size = item['size']
        conv = float(size) / float(price)
        if item['side'] == 'Buy':
            buy_total += conv
            buy_total_size += size
            buy_data.append(item)
        elif item['side'] == 'Sell':
            sell_data.append(item)
            sell_total += conv
            sell_total_size += size
# нужн добавить точности

        print('Buy Amount:')
        print(buy_total)
        print('Sell Amount:')
        print(sell_total)
        print ('TOTAL:')
        total = buy_total_size - sell_total_size

    if total < 0:
         dawnflag += 1
         point = '\u2193'
         #print('Капитализация уменьшена на : '+ str(total * -1 ) + '$'+'\u2193')
    elif total > 0:
          upflag += 1
          if total > 30:
           print('Капитализация увеличена на : ' +  str(total) + '$' + '\u2191')
          #print('Капитализация увеличена на : ' +  str(total) + '$' + '\u2191')
           point = '\u2191'
          else:
           point = '\u2191'

    print('Прогноз :' + point)
    print('Bybit :' + str(price))
    print('DawnFlag:' + str(dawnflag))
    print('UPFlag:' + str(upflag))
    prices()
    time.sleep(5)
