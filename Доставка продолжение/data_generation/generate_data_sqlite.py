import sqlite3
from faker import Faker
import random

# Генератор случайных данных
fake = Faker()

# Создаем соединение с SQLite
conn = sqlite3.connect('courier_delivery_db.sqlite')
cursor = conn.cursor()

# Удаляем старую таблицу, если она существует
cursor.execute('DROP TABLE IF EXISTS full_info')

# Создаем таблицу с объединенной информацией (без пароля)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS full_info (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        user_nickname TEXT,
        user_full_name TEXT,
        address_from TEXT,
        address_to TEXT,
        coordinates_from TEXT,
        coordinates_to TEXT,
        track_number TEXT,
        invoice_price INTEGER,
        courier_price INTEGER,
        commission INTEGER
    )
''')

# Функция для генерации случайных данных
def generate_data():
    # Генерация 10 пользователей
    users = []
    for _ in range(10):
        full_name = fake.name()  # Генерируем полное имя (ФИО)
        users.append({'full_name': full_name, 'nickname': fake.user_name()})

    # Генерация 2000 заказов с информацией
    for _ in range(2000):
        user = random.choice(users)
        user_full_name = user['full_name']  # Полное имя пользователя (ФИО)
        user_nickname = user['nickname']
        address_from = fake.address().replace("\n", ", ")
        address_to = fake.address().replace("\n", ", ")
        coordinates_from = f"Долгота: {random.uniform(-180, 180):.6f}, Широта: {random.uniform(-90, 90):.6f}"
        coordinates_to = f"Долгота: {random.uniform(-180, 180):.6f}, Широта: {random.uniform(-90, 90):.6f}"
        track_number = fake.uuid4()
        invoice_price = random.randint(1000, 10000)  # Натуральная цена (например, в тенге)
        courier_price = random.randint(100, 1000)    # Натуральная цена
        commission = random.randint(50, 500)         # Натуральная комиссия
        
        # Вставляем данные в новую объединенную таблицу
        cursor.execute('''
            INSERT INTO full_info (user_nickname, user_full_name, address_from, address_to, coordinates_from, coordinates_to, track_number, invoice_price, courier_price, commission)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_nickname, user_full_name, address_from, address_to, coordinates_from, coordinates_to, track_number, invoice_price, courier_price, commission))
    
    conn.commit()
    print("Данные успешно сгенерированы!")

# Запуск генерации данных
generate_data()

# Закрытие соединения
conn.close()
