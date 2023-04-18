import requests
import numpy
import time
from PIL import Image
from playwright.sync_api import sync_playwright
url = "https://www.coinglass.com/ru/merge/BTC-USDT"
screen_size =(0,0,480,750)
exchanges = {
    "Binance": "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
    "Coinbase": "https://api.coinbase.com/v2/prices/BTC-USD/spot",
    "Bitfinex": "https://api.bitfinex.com/v1/pubticker/BTCUSD",
    "Kraken": "https://api.kraken.com/0/public/Ticker?pair=XBTUSD",
    "Bitstamp": "https://www.bitstamp.net/api/v2/ticker/btcusd/"
}

def click_icon(page):
    icon_selector =  'svg[data-icon="close-circle"]'
    icon = page.locator(icon_selector)
    icon.click()
def get_book_btc():
  with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url)
    page.evaluate("window.scrollBy(0, 190)")
    click_icon(page)
    time.sleep(2)
    page.screenshot(path="screenshot.png")
    browser.close()
    screenshot = Image.open('screenshot.png')
    cropped_screenshot = screenshot.crop(screen_size)
    cropped_screenshot.save('screenshot.png')

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
