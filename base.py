import sqlite3
import datetime
conn = sqlite3.connect('bot.db')
c = conn.cursor()
baza = 'bot.db'

def base_create():
 c.execute('''CREATE TABLE IF NOT EXISTS users
             (user_id INTEGER PRIMARY KEY, username TEXT, apikey TEXT, kit TEXT,kit_amount TEXT
             , Orderbook TEXT, Notification_type TEXT, Notification_amount TEXT
             , Notification_fixed TEXT, Currency TEXT,interval TEXT,state TEXT )''')
 conn.commit()

 c.execute('''CREATE TABLE IF NOT EXISTS kit
             (id INTEGER PRIMARY KEY AUTOINCREMENT, hash TEXT, amount TEXT, am_usd TEXT,tr_time TEXT
             , my_time TEXT, transaction_full_hash TEXT, sender TEXT
             , getters TEXT )''')
 conn.commit()
 conn.close()
def check_user(user_id):

    conn = sqlite3.connect(baza)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    if result[0] == 0:
        return False
    else:
        return True
def set_user_settings(user_id, apikey=None, kit = None
                      ,kit_amount=None, Orderbook = None,Notification_type=None,Notification_amount=None
                      ,Notification_fixed=None,Currency=None,interval=None,state=None):
    conn = sqlite3.connect(baza)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    if result[0] == 0:
        # user_id does not exist, insert new record
        c.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
        conn.commit()

    if apikey is not None:
        c.execute('UPDATE users SET apikey = ? WHERE user_id = ?', (apikey, user_id))
        conn.commit()
    if kit is not None:
        c.execute('UPDATE users SET kit = ? WHERE user_id = ?', (kit, user_id))
        conn.commit()
    if kit_amount is not None:
        c.execute('UPDATE users SET kit_amount = ? WHERE user_id = ?', (kit_amount, user_id))
        conn.commit()
    if Orderbook is not None:
        c.execute('UPDATE users SET Orderbook = ? WHERE user_id = ?', (Orderbook, user_id))
        conn.commit()
    if Notification_type is not None:
        c.execute('UPDATE users SET Notification_type = ? WHERE user_id = ?', (Notification_type, user_id))
        conn.commit()
    if Notification_amount is not None:
        c.execute('UPDATE users SET Notification_amount = ? WHERE user_id = ?', (Notification_amount, user_id))
        conn.commit()
    if Notification_fixed is not None:
        c.execute('UPDATE users SET Notification_fixed = ? WHERE user_id = ?', (Notification_fixed, user_id))
        conn.commit()
    if Currency is not None:
        c.execute('UPDATE users SET Currency = ? WHERE user_id = ?', (Currency, user_id))
        conn.commit()
    if interval is not None:
        c.execute('UPDATE users SET interval = ? WHERE user_id = ?', (interval, user_id))
        conn.commit()
    if kit_amount is not None:
        c.execute('UPDATE users SET kit_amount = ? WHERE user_id = ?', (kit_amount, user_id))
        conn.commit()
    if state is not None:
        c.execute('UPDATE users SET state = ? WHERE user_id = ?', (state, user_id))
        conn.commit()


    conn.close()

def get_user_setting(user_id, param):
    conn = sqlite3.connect(baza)
    c = conn.cursor()
    c.execute(f'SELECT {param} FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()

    return result if result else None
def check_table_users():
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    result = c.fetchone()

    if result is not None:
        c.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in c.fetchall()]

        # проверяем, что все нужные столбцы присутствуют в таблице
        if 'user_id' in columns and 'username' in columns and 'apikey' in columns and 'kit' in columns and \
                'kit_amount' in columns and 'Orderbook' in columns and 'Notification_type' in columns and \
                'Notification_amount' in columns and 'Notification_fixed' in columns and 'Currency' in columns\
                and 'interval' in columns and 'kit_amount' in columns :
            print("Table 'users' exists with required columns.")
        else:
            print("Table 'users' exists but does not have all required columns.")
            print(columns)
    else:
        print("Table 'users' does not exist.")
        base_create()
    conn.close()
'''
(id INTEGER PRIMARY KEY AUTOINCREMENT, hash TEXT, amount TEXT, am_usd TEXT,tr_time TEXT
             , my_time TEXT, transaction_full_hash TEXT, sender TEXT
             , getters TEXT )
'''
def kit_save(data):
    hash = data[0]
    amount_btc = data[2]
    ti = data[1]
    tr_time = ti[0:len(ti) - 1]
    amount_usd = data[3]
    time = datetime.datetime.now()
    my_time = time.strftime("%H:%M:%S")
    trans_fh = data[4]
    #print(trans_fh)
    conn = sqlite3.connect(baza)
    c = conn.cursor()
    c.execute("INSERT INTO kit (hash,amount,am_usd,tr_time,my_time,transaction_full_hash) VALUES (?,?,?,?,?,?)",(hash,amount_btc,amount_usd,tr_time,my_time,trans_fh))
    conn.commit()
    conn.close()
def kit_checked_wallet(data):

    hash = data[0]
    trans_full_hash = data[1]
    sender = data[2]
    getters = data[3]
    conn = sqlite3.connect(baza)
    c = conn.cursor()
    c.execute("UPDATE kit SET transaction_full_hash = ?, sender = ?, getters = ? WHERE hash = ?", (trans_full_hash,sender,getters, hash))
    conn.commit()
    conn.close()


def get_users_kit():
    # Подключение к базе данных
    conn = sqlite3.connect(baza)
    cursor = conn.cursor()
    # Выборка всех пользователей с флагом функции, установленным в True
    cursor.execute("SELECT user_id FROM users WHERE kit = 1")
    result = cursor.fetchall()
    conn.close()
    return result
def get_users_price_attention():
    # Подключение к базе данных
    conn = sqlite3.connect(baza)
    cursor = conn.cursor()
    # Выборка всех пользователей с флагом функции, установленным в True
    cursor.execute("SELECT user_id FROM users WHERE Orderbook= 1")
    result = cursor.fetchall()
    conn.close()
    return result



