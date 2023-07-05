import time
from PIL import Image
from playwright.sync_api import sync_playwright
url = "https://www.coinglass.com/ru/merge/BTC-USDT"
screen_size =(0,0,480,750)
async def click_icon(page):
    icon_selector =  'svg[data-icon="close-circle"]'
    icon = page.locator(icon_selector)
    await icon.click()

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
