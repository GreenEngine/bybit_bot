import PIL.Image
import requests
import commands
from telegram import Update,InputMediaPhoto
from telegram.ext import Updater, CommandHandler, CallbackContext , Application,ContextTypes
import io
import base
# Установите токен бота, полученный от BotFather
TOKEN = ''
# необходимо добавить функцию отслеживания кита
'''
добавить шифрованиебазы
Необходмы настройки оповещений 
цены 
площадки 
ордера 
график 
'''
# Исправить оповещения
# Установите URL-адрес API Bybit
BASE_URL = 'https://api.bybit.com'
global kit_scaner_on
kit_scaner_on = ('_',)
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
base.base_create()
base.check_table_users()
# Создайте обработчик команды /start
async def start(update: Update, context: CallbackContext) -> None:
    base.set_user_settings(user_id=update.effective_chat.id, apikey='0', kit = '0'
                      ,kit_amount='50', Orderbook = '1',Notification_type='change',Notification_amount='100'
                      ,Notification_fixed='0',Currency='BTC',interval='10')
    await update.message.reply_text(
    'Добро пожаловать! Это бот для получения курса валюты с Bybit. Введите /help для получения списка команд.')

##`sjevM3xG9qgFE6b
async def send_notification(context):
    global last_price
    chat= context.message.chat_id
    notification_amount = base.get_user_setting(chat,'notification_amount')
    print('Send Notification')
    selected_currency = base.get_user_setting(chat,'Currency')
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
    notification_type = base.get_user_setting(chat,'notification_type')
    # Проверьте, что тип уведомлений выбран корректно и отправьте уведомление
    if notification_type == 'change' and abs(price_change) > notification_amount:
       last_price = price
       await context.bot.send_message(chat_id=chat, text=f' {selected_currency}.:{price}$ \n :{price_change}$')

async def check_kit(context) :
       chat_id = job.chat_id
       #print(str(chat_id))
       data = commands.kit_check(chat_id)
       if data is not None:
           hash = data[0]
           crypto = data[2]
           ti = data[1]
           usd = data[3]
           mess = f'BTC:{crypto}\nUsd:{usd}\nВремя:{ti}'
           await context.bot.send_message(chat_id=chat_id, text=f'Проплыл кит:\n{mess}$')
           #хочу чтобы бот отправлял ссылку на кошелек
           data = None
async def kit_attention(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    kit_scaner_on = base.get_user_setting(chat_id,'kit')
    global job
    poll_interval = base.get_user_setting(chat_id,'interval')


    if job is not None:
        kit_scaner_on = base.set_user_settings(user_id=chat_id, kit='1')

        await update.message.reply_text('Функция оповещения о крупных транзакциях  выключена ')
    if context.job_queue:
       job = context.job_queue.run_repeating(callback=check_kit,interval=5,chat_id =chat_id)
    else:
        print('fail initalize')
    if  kit_scaner_on == '1':
        base.set_user_settings(user_id=chat_id, kit='0')

    else:
        base.set_user_settings(user_id=chat_id, kit='1')
        await update.message.reply_text('Функция оповещения о крупных транзакциях  включена')



    # Проверьте, что задача отправки уведомлений еще не запущена

    # Запустите задачу отправки уведомлений



# Создайте обработчик команды /help
async def help(update: Update, context: CallbackContext) -> None:
    help_text =("Этот бот позволяет получить текущий курс валюты с Bybit."

    +"\n Список команд:"

    +"\n/start - Начать работу с ботом"
    +"\n/help - Получить список команд"
    +"\n/currency - Изменить выбранную валюту"
    +"\n/price - Получить текущий курс выбранной валюты"
    +"\n/interval - Изменить интервал опроса курса валюты"
    +"\n/notification_type - Изменить тип уведомлений"
    +"\n/notification_amount - Изменить сумму изменения курса уведомлений"
    +"\n/start_timer - Запустить таймер уведомлений"
    +"\n/stop_timer - Остановить таймер уведомлений"
    +"\n/kit_attention - включить оповещение о китах"
    +"\n/kit_amount - размер кита")



    await update.message.reply_text(help_text)

async def set_kit(update: Update, context: CallbackContext) -> None:

    # Извлеките выбранную валюту из аргумента команды
    kit_amm = context.args[0].upper()
    # Проверьте, что выбранная валюта допустима
    # Обновите выбранную валюту
    base.set_user_settings(user_id=update.effective_chat.id,kit_amount=kit_amm)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Вы выбрали размер кита: {kit_amm}')
# Создайте обработчик команды /currency
async def set_currency(update: Update, context: CallbackContext) -> None:

    # Извлеките выбранную валюту из аргумента команды
    currency = context.args[0].upper()
    # Проверьте, что выбранная валюта допустима
    if currency not in ['BTC', 'ETH', 'EOS', 'XRP']:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Извините, эту валюту не поддерживается. Пожалуйста, выберите другую валюту.')
        return
    # Обновите выбранную валюту
    base.set_user_settings(user_id=update.effective_chat.id,Currency=currency)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Выбрана валюта: {selected_currency}')

# Создайте обработчик команды /price
async def get_price(update: Update, context: CallbackContext) -> None:
    # Создайте URL-адрес для запроса курса выбранной валюты
    url = f'{BASE_URL}/v2/public/tickers?symbol={selected_currency}USD'
    # Отправьте GET-запрос на URL-адрес
    pr = commands.prices()
    message = f'\n{pr[0]}\n{pr[1]}\n{pr[2]}\n{pr[3]}\n'
    response = requests.get(url)
    # Извлеките цену выбранной валюты из ответа
    price = response.json()['result'][0]['last_price']
    global last_price
    last_price = price
    await commands.get_book_btc()
    photo = PIL.Image.open('screenshot.png')
    with io.BytesIO() as output:
        photo.save(output, format='PNG')
        image_data = output.getvalue()
    await context.bot.send_message(chat_id=update.effective_chat.id,text=f'\n Bybit: {selected_currency}: {price}{message}')
    await context.bot.sendPhoto(chat_id = update.effective_chat.id , photo=image_data)
# Создайте обработчик команды /interval
async def set_interval(update: Update, context: CallbackContext) -> None:
    # Извлеките интервал опроа из аргумента команды
    interval = int(context.args[0])
    # Проверьте, что интервал опроса не меньше 10 секунд
    if interval < 10:
      await  context.bot.send_message(chat_id=update.effective_chat.id, text='Извините, интервал опроса не может быть меньше 10 секунд.')
      return
    # Обновите интервал опроса
    base.set_user_settings(user_id=update.effective_chat.id,interval=interval)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Интервал опроса изменен на {interval} секунд.')

# Создайте обработчик команды /notification
async def set_notification_type(update: Update, context: CallbackContext) -> None:
    # Извлеките тип уведомлений из аргумента команды
    notification = context.args[0]

    # Проверьте, что тип уведомлений допустим
    if notification not in ['change', 'percentage', 'amount']:
       await  context.bot.send_message(chat_id=update.effective_chat.id, text='Извините, этот тип уведомлений не поддерживается. Пожалуйста, выберите другой тип уведомлений.')
       return
    # Обновите тип уведомлений
    base.set_user_settings(user_id=update.effective_chat.id, Notification_type=notification)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Выбран тип уведомлений: {notification}')

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
    chat = update.effective_chat.id
    user = update.message.from_user
    text = update.message.text.split()
    if len(text) > 1:
        amount = float(text[1])
        context.user_data['notification_amount'] = amount
        base.set_user_settings(user_id=chat,Notification_amount=amount)
        message = f"{user.first_name}, оповещения будут приходить, если курс изменится на {amount:.2f}"
    else:
        message = f"{user.first_name}, необходимо указать сумму изменения курса. Например, /notification_amount 100.00"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def send_notification(context ) :
    global last_price
    chat = context.message.chat_id
    notification_amount = base.get_user_setting(chat,'notification_amount')
    print('Send Notification')
    selected_currency = base.get_user_setting(chat,'Currency')
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

    # Проверьте, что тип уведомлений выбран корректно и отправьте уведомление
    if notification_type == 'change' and abs(price_change) > notification_amount:
       last_price = price
       await context.bot.send_message(chat_id=chat, text=f' {selected_currency}.:{price}$ \n :{price_change}$')



    # Обновите последнюю цену выбранной валюты

async def start_timer(update: Update, context: CallbackContext):
    global job
    chat = update.message.chat_id
    interval = base.get_user_setting(chat,'interval')
    # Проверьте, что задача отправки уведомлений еще не запущена
    if job is not None:
       await  context.bot.send_message(chat_id=chat, text='Извините, задача отправки уведомлений уже запущена.')
       return
    # Запустите задачу отправки уведомлений
    if context.job_queue:
       job = context.job_queue.run_repeating(callback=send_notification,interval=interval, chat_id =chat )
    else:
        print('fail initalize')

    await context.bot.send_message(chat_id=chat, text=f'Задача отправки уведомл')

# Создайте функцию для запуска бота
def main() -> None:
    print('one')
    # Создайте объект Updater и передайте ему токен бота
    application = Application.builder().token(TOKEN).build()
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
    application.add_handler(CommandHandler('kit_attention', kit_attention))
    application.add_handler(CommandHandler('kit_amount', set_kit))
    # Добавьте обработчик команды /stop_timer
    application.add_handler(CommandHandler('stop_timer', stop_timer))

    # Запустите бота
    application.run_polling()

    # Войдите в цикл получения обновлений


if __name__ == '__main__':
    main()

