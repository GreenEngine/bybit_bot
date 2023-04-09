
import requests
from PIL import Image

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext , Application,ContextTypes
import sqlite3
# Установите токен бота, полученный от BotFather
TOKEN = '5028082776:AAGRWWC7LmLNg0HsHGkSDhLsiCPMPhdDu9U'
# Установите URL-адрес API Bybit
BASE_URL = 'https://api.bybit.com'
#bybit api key - 0po7hx9wvnoZsK8cGa
#secret key - iN1hxxD0oefDo1sVk2XBik7wIRZj68IzcqgD
# Создайте экземпляр класса Updater и передайте ему токен бота
global notification_type
notification_type = 'change'
global notification_amount
notification_amount = 100
global poll_interval
poll_interval = 10
global last_price
# Создайте глобальные переменные для выбранной валюты, интервала опроса, типа уведомлений и задачи отправки уведомлений
selected_currency = 'BTC'

job = None


# Создайте обработчик команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
    'Добро пожаловать! Это бот для получения курса валюты с Bybit. Введите /help для получения списка команд.')

##`sjevM3xG9qgFE6b


# Создайте обработчик команды /help
async def help(update: Update, context: CallbackContext) -> None:
    help_text =("Этот бот позволяет получить текущий курс валюты с Bybit."

    +"\n Список команд:"

    +"\n/start - Начать работу с ботом"
    +"\n/help - Получить список команд"
    +"\n/currency - Изменить выбранную валюту"
    +"\n/price - Получить текущий курс выбранной валюты"
    +"\n/interval - Изменить интервал опроса курса валюты"
    +"\n/notification - Изменить тип уведомлений"
    +"\n/start_timer - Запустить таймер уведомлений"
    +"\n/stop_timer - Остановить таймер уведомлений")


    await update.message.reply_text(help_text)


# Создайте обработчик команды /currency
async def set_currency(update: Update, context: CallbackContext) -> None:
    global selected_currency
    # Извлеките выбранную валюту из аргумента команды
    currency = context.args[0].upper()
    # Проверьте, что выбранная валюта допустима
    if currency not in ['BTC', 'ETH', 'EOS', 'XRP']:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Извините, эту валюту не поддерживается. Пожалуйста, выберите другую валюту.')
        return
    # Обновите выбранную валюту
    selected_currency = currency
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Выбрана валюта: {selected_currency}')

# Создайте обработчик команды /price
async def get_price(update: Update, context: CallbackContext) -> None:
    # Создайте URL-адрес для запроса курса выбранной валюты
    url = f'{BASE_URL}/v2/public/tickers?symbol={selected_currency}USD'
    # Отправьте GET-запрос на URL-адрес
    response = requests.get(url)
    # Извлеките цену выбранной валюты из ответа
    price = response.json()['result'][0]['last_price']
    global last_price
    last_price = price
    # Отправьте цену выбранной валюты в чат
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Текущий курс {selected_currency}: {price}')

# Создайте обработчик команды /interval
async def set_interval(update: Update, context: CallbackContext) -> None:
    global poll_interval
    # Извлеките интервал опроа из аргумента команды
    interval = int(context.args[0])
    # Проверьте, что интервал опроса не меньше 10 секунд
    if interval < 10:
      await  context.bot.send_message(chat_id=update.effective_chat.id, text='Извините, интервал опроса не может быть меньше 10 секунд.')
      return
    # Обновите интервал опроса
    poll_interval = interval
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Интервал опроса изменен на {poll_interval} секунд.')

# Создайте обработчик команды /notification
async def set_notification_type(update: Update, context: CallbackContext) -> None:
    global notification_type
    # Извлеките тип уведомлений из аргумента команды
    notification = context.args[0]

    # Проверьте, что тип уведомлений допустим
    if notification not in ['change', 'percentage', 'amount']:
       await  context.bot.send_message(chat_id=update.effective_chat.id, text='Извините, этот тип уведомлений не поддерживается. Пожалуйста, выберите другой тип уведомлений.')
       return
    # Обновите тип уведомлений
    notification_type = notification
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Выбран тип уведомлений: {notification_type}')

# Создайте обработчик команды /start_timer
# Создайте обработчик команды /stop_timer
async def stop_timer(update: Update, context: CallbackContext) -> None:
    global job
    # Проверьте, что задача отправки уведомлений запущена
    if job is None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Извините, задача отправки уведомлений еще не запущена.')
        return
    # Остановите задачу отправки уведомлений
    job.schedule_removal()
    job = None

    await context.bot.send_message(chat_id=update.effective_chat.id, text='Задача отправки уведомлений остановлена.')

# Создайте функцию для отправки уведомлений
async def set_notification_amount(update, context):
    global notification_amount
    user = update.message.from_user
    text = update.message.text.split()
    if len(text) > 1:
        amount = float(text[1])
        notification_amount = amount
        context.user_data['notification_amount'] = amount
        message = f"{user.first_name}, оповещения будут приходить, если курс изменится на {amount:.2f}"
    else:
        message = f"{user.first_name}, необходимо указать сумму изменения курса. Например, /notification_amount 100.00"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def send_notification(context ) :
    global last_price
    global notification_amount
    global chat
    print('Send Notification')

    # Создайте URL-адрес для запроса курса выбранной валюты
    url = f'{BASE_URL}/v2/public/tickers?symbol={selected_currency}USD'
    # Отправьте GET-запрос на URL-адрес
    response = requests.get(url)
    # Извлеките цену выбранной валюты из ответа
    price = response.json()['result'][0]['last_price']
    print(f'{price}')
    # Вычислите изменение цены выбранной валюты с момента последнего запроса
    price_change = float(price) - float(last_price)
    # Вычислите процент изменения цены выбранной валюты с момента последнего запроса
    percentage_change = (float(price) - float(last_price)) / float(last_price) * 100
    # Проверьте, что тип уведомлений выбран корректно и отправьте уведомление
    if  notification_type == 'change' and abs(price_change) > notification_amount:
       last_price = price
       await context.bot.send_message(chat_id=chat, text=f'Цена {selected_currency} изменилась на {price_change}. \n Текущая цена:{price}')
    elif notification_type == 'percentage' and abs(percentage_change) > notification_amount:
       await context.bot.send_message(chat_id=chat, text=f'Цена {selected_currency} изменилась на {percentage_change}%.')
    elif notification_type == 'amount' and abs(price_change) > notification_amount:
       await  context.bot.send_message(chat_id=chat, text=f'Цена {selected_currency} изменилась на {price_change}.')
    # Обновите последнюю цену выбранной валюты

async def start_timer(update: Update, context: CallbackContext):
    global job
    global poll_interval
    global chat

    chat = update.message.chat_id
    # Проверьте, что задача отправки уведомлений еще не запущена
    if job is not None:
       await  context.bot.send_message(chat_id=update.effective_chat.id, text='Извините, задача отправки уведомлений уже запущена.')
       return
    # Запустите задачу отправки уведомлений
    job = context.job_queue.run_repeating(callback=send_notification,interval=poll_interval, chat_id =update.message.chat_id )

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Задача отправки уведомл')

# Создайте функцию для запуска бота
def main() -> None:
    print('one')
    # Создайте объект Updater и передайте ему токен бота
    application = Application.builder().token(TOKEN).build()

    # Получите объект Dispatcher из объекта Updater


    # Добавьте обработчик команды /start
    application.add_handler(CommandHandler('start', start))

    # Добавьте обработчик команды /help
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('currency', set_currency))

    # Добавьте обработчик команды /price
    application.add_handler(CommandHandler('price', get_price))

    # Добавьте обработчик команды /interval
    application.add_handler(CommandHandler    ('interval', set_interval))

    # Добавьте обработчик команды /notification_type
    application.add_handler(CommandHandler('notification_type', set_notification_type))

    # Добавьте обработчик команды /notification_amount
    application.add_handler(CommandHandler('notification_amount', set_notification_amount))

    # Добавьте обработчик команды /start_timer
    application.add_handler(CommandHandler('start_timer', start_timer))

    # Добавьте обработчик команды /stop_timer
    application.add_handler(CommandHandler('stop_timer', stop_timer))

    # Запустите бота
    application.run_polling()

    # Войдите в цикл получения обновлений

    print('start')

if __name__ == '__main__':
    main()