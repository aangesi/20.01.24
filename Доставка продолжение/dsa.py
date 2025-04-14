import sqlite3

# Подключаемся к базе данных SQLite
conn = sqlite3.connect('courier_delivery_db.sqlite')
cursor = conn.cursor()

# Проверяем наличие таблицы 'User'
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='User';")
result = cursor.fetchone()

if result:
    print("Таблица 'User' существует.")
else:
    print("Таблица 'User' не найдена.")

conn.close()
