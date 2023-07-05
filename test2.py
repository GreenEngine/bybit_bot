import requests
from bs4 import BeautifulSoup
import time
import re
url = "https://www.blockchain.com/explorer/mempool/btc"
kit = 30
kits = []
last_trans = ('1','1','1','1')
while True:

    # Отправляем запрос на получение HTML-кода страницы
    response = requests.get(url)

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
            #здесь можно добавить тригер на срабатывание
            #тут же можно добавить клик в браузере для перехода в транзакцию и считывание кошелька
         else:

           # print(f'Транзкция {trans[0]} уже была добавлена')
            break
         #print(f'{kits} \n')
    time.sleep(1)