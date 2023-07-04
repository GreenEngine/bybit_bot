import requests
from bs4 import BeautifulSoup
import base
import ccxt
import pandas as pd
import mplfinance as mpf
import time
import re
kiturl = "https://www.blockchain.com/explorer/mempool/btc"
kits = []
global last_trans
last_trans = ('1','1','1','1')
import asyncio
from PIL import Image
from playwright.async_api import async_playwright
from playwright._impl._api_types import Error
url = "https://www.coinglass.com/ru/merge/BTC-USDT"
screen_size =(0,0,480,750)
exchanges = {
    "Binance": "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
    "Coinbase": "https://api.coinbase.com/v2/prices/BTC-USD/spot",
    "Bitfinex": "https://api.bitfinex.com/v1/pubticker/BTCUSD",
    "Kraken": "https://api.kraken.com/0/public/Ticker?pair=XBTUSD",
    "Bitstamp": "https://www.bitstamp.net/api/v2/ticker/btcusd/"
}

async def click_icon(page):
    icon_selector = 'svg[data-icon="close-circle"]'
    icon = page.locator(icon_selector)
    await icon.click()

async def get_book_btc():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        await page.evaluate("window.scrollBy(0, 190)")

        await asyncio.sleep(2)
        await page.screenshot(path="screenshot.png")
        await browser.close()
        screenshot = Image.open('screenshot.png')
        cropped_screenshot = screenshot.crop(screen_size)
        cropped_screenshot.save('screenshot.png')
        screenshot.close()
        cropped_screenshot.close()
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

def kit_check(chat):
    #print("kit")
    links = []

    kit = base.get_user_setting(chat,'kit_amount')

    global last_trans
    # Отправляем запрос на получение HTML-кода страницы
    response = requests.get(kiturl)

    # Парсим HTML-код страницы с помощью BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Находим необходимые данные на странице
    data = soup.find("div", {"class": "sc-7b53084c-1 czXdjN"}).text
    link = soup.find_all("a", href=lambda href: href and "explorer/transactions/btc" in href)
    for l in link:
     links.append(l["href"])#добавляем ссылки в список
    # Разделяем данные на отдельные строки, используя "Hash" в качестве разделителя
    transactions = data.split("Hash ")[1:]

    # Итерируемся по транзакциям и выводим их данные
    for transaction in transactions:
        # Разделяем строку транзакции на отдельные элементы
        elements = transaction.split()

        # Извлекаем сумму в биткоинах и долларах
        btc_amount = elements[-2]
        timed = btc_amount[0:8]
        btc_amount = btc_amount[8:len(btc_amount)]
        usd_amount = elements[-1]
        usd_amount = usd_amount[4:len(usd_amount)]
        hash = elements[0]
        hash = hash[0:9]
        trans = (hash,timed,btc_amount,usd_amount)
        if float(btc_amount) >= float(kit[0]):
         if trans[0] != last_trans[0]:
           last_trans = trans
           if trans in kits:
               #print(f'Транзкция {trans[0]} уже была добавлена')
               break
           else:
            kits.append(trans)
           # print(trans)
            print('kit_trnas')
           # print(trans[0])
            for l in links:
               # print(l)
                l = l[27:]
                #print(l)
                tr = trans[0]
                tr1 = tr[0:4]
                tr2 = tr[5:]
                #print(tr1)
                if l.startswith(tr1) and l.endswith(tr2):
                    #print(trans)
                    trans = trans +(l,)
                    #print(trans)
                    base.kit_save(trans)
            #здесь нужно изскать этот хеш и  добавлять данные в базу
            return trans
            #тут же можно добавить клик в браузере для перехода в транзакцию и считывание кошелька
         else:

           # print(f'Транзкция {trans[0]} уже была добавлена')
            print('kit_none')
            return None
         #print(f'{kits} \n')
def get_graph():
    exchange = ccxt.bybit()

    # Получите данные графика для определенной криптовалютной пары и временного интервала
    symbol = 'BTC/USDT'
    timeframe = '30m'
    limit = 50  # Максимальное количество свечей, которые можно запросить за один раз
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)

    # Преобразуйте данные в удобный формат для анализа, используя библиотеку Pandas
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)

    # Отобразите свечной график с помощью библиотеки mplfinance
    mpf.plot(df, type='candle', volume=True, style='charles', savefig='graph.png')
    return Image.open('graph.png')
