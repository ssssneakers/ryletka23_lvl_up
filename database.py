import sqlite3
from config import DB_FILE1, user_money
import logging

path_to_db1 = DB_FILE1  # файл базы данных


async def create_database():
    try:
        # подключаемся к базе данных
        with sqlite3.connect(path_to_db1) as conn:
            cursor = conn.cursor()
            # создаём таблицу messages
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_database (
                user_id INTEGER PRIMARY KEY,
                user_money INTEGER,
                user_name TEXT,
                user_trade TEXT)
            ''')
            logging.info("DATABASE: База данных 1 создана")  # делаем запись в логах
    except Exception as e:
        print(e)
        return None


async def add_message(user_id, username):
    try:
        # подключаемся к базе данных
        with sqlite3.connect(path_to_db1) as conn:
            cursor = conn.cursor()
            # создаём таблицу messages
            cursor.execute('''
                INSERT INTO user_database (user_id, user_money, user_name, user_trade)
                VALUES (?, ?, ?, ?)
            ''', (user_id, user_money, username, ''))
            logging.info("DATABASE: База данных 1 создана")  # делаем запись в логах
    except Exception as e:
        print(e)
        return

async def check_username(username):
    try:
        with sqlite3.connect(path_to_db1) as conn:
            cursor = conn.cursor()
            # выполняем запрос к базе данных
            cursor.execute('SELECT user_money FROM user_database WHERE user_name=?', (username,))
            logging.info("DATABASE: Пользователь в поиске")  # делаем запись в логах
            return cursor.fetchone()
    except Exception as e:
        logging.error("Ошибка в базе данных: ", e)  # если ошибка - записываем её в логи
        return

async def check_user_id(username):
    try:
        with sqlite3.connect(path_to_db1) as conn:
            cursor = conn.cursor()
            # выполняем запрос к базе данных
            cursor.execute('SELECT user_id FROM user_database WHERE user_name=?', (username,))
            logging.info("DATABASE: Пользователь в поиске")  # делаем запись в логах
            return cursor.fetchone()
    except Exception as e:
        logging.error("Ошибка в базе данных: ", e)  # если ошибка - записываем её в логи
        return

async def check_user_name(user_id):
    try:
        with sqlite3.connect(path_to_db1) as conn:
            cursor = conn.cursor()
            # выполняем запрос к базе данных
            cursor.execute('SELECT user_name FROM user_database WHERE user_id=?', (user_id,))
            logging.info("DATABASE: Пользователь в поиске")  # делаем запись в логах
            return cursor.fetchone()
    except Exception as e:
        logging.error("Ошибка в базе данных: ", e)  # если ошибка - записываем её в логи
        return

async def check_user_top(user_id):
    try:
        # подключаемся к базе данных
        with sqlite3.connect(path_to_db1) as conn:
            cursor = conn.cursor()
            # выполняем запрос к базе данных
            cursor.execute('''
                SELECT COUNT(*) FROM user_database
                WHERE user_id = ?
            ''', (user_id,))
            logging.info("DATABASE: Пользователь в поиске")  # делаем запись в логах
            return cursor.fetchone()
    except Exception as e:
        logging.error("Ошибка в базе данных: ", e)  # если ошибка - записываем её в логи
        return


async def get_balance(user_id):
    try:
        with sqlite3.connect(path_to_db1) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT user_money FROM user_database
                WHERE user_id = ?
            ''', (user_id,))
            return cursor.fetchone()[0]
    except Exception as e:
        print(e)


async def edit_balance(user_id, user_balance):
    try:
        with sqlite3.connect(path_to_db1) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE user_database
                SET user_money = ?
                WHERE user_id = ?
            ''', (user_balance, user_id))
    except Exception as e:
        print(e)

async def get_all_balance():
    try:
        with sqlite3.connect(path_to_db1) as conn:
            cursor = conn.cursor()
            # Измените запрос, чтобы получить идентификатор пользователя и его баланс
            cursor.execute('''
                SELECT user_id, user_money FROM user_database
            ''')
            return cursor.fetchall()
    except Exception as e:
        print(e)

async def get_all_balance_name():
    try:
        with sqlite3.connect(path_to_db1) as conn:
            cursor = conn.cursor()
            # Измените запрос, чтобы получить идентификатор пользователя и его баланс
            cursor.execute('''
                SELECT user_name, user_money FROM user_database
            ''')
            return cursor.fetchall()
    except Exception as e:
        print(e)

async def get_user_rank(user_id):
    try:
        all_user_balance = await get_all_balance()
        # Убедитесь, что сортировка выполняется по балансу (второй элемент кортежа)
        sorted_balance = sorted(all_user_balance, key=lambda x: x[1], reverse=True)
        # Теперь словарь рангов будет создан правильно
        user_ranks = {uid: rank for rank, (uid, _) in enumerate(sorted_balance, start=1)}
        # Возвращаем ранг пользователя
        return user_ranks.get(user_id)
    except Exception as e:
        print(e)


async def get_top():
    try:
        with sqlite3.connect(path_to_db1) as conn:
            cursor = conn.cursor()
            # Изменен запрос для выборки имени пользователя и его денег
            cursor.execute('''
                SELECT user_name, user_money FROM user_database
                ORDER BY user_money DESC, user_name
                LIMIT 10
            ''')
            return cursor.fetchall()
    except Exception as e:
        print(e)
