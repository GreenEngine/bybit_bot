import requests
from bs4 import BeautifulSoup
import time
import re
kiturl = "https://www.blockchain.com/explorer/mempool/btc"
kit = 1
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
    icon_selector =  'svg[data-icon="close-circle"]'
    icon = page.locator(icon_selector)
    await icon.click()
async def get_book_btc():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        await page.evaluate("window.scrollBy(0, 190)")
        await click_icon(page)
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

def kit_check():
    print("kit")
    global last_trans
    # Отправляем запрос на получение HTML-кода страницы
    response = requests.get(kiturl)

    # Парсим HTML-код страницы с помощью BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Находим необходимые данные на странице
    data = soup.find("div", {"class": "sc-7b53084c-1 czXdjN"}).text
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
        hash = hash[0:10]
        trans = (hash,timed,btc_amount,usd_amount)
        if float(btc_amount) >= kit:
         if trans[0] != last_trans[0]:
           last_trans = trans
           if trans in kits:
               #print(f'Транзкция {trans[0]} уже была добавлена')
               break
           else:
            kits.append(trans)
            print(trans)
            print('kit_trnas')
            return trans
            #тут же можно добавить клик в браузере для перехода в транзакцию и считывание кошелька
         else:

           # print(f'Транзкция {trans[0]} уже была добавлена')
            print('kit_none')
            return None
         #print(f'{kits} \n')