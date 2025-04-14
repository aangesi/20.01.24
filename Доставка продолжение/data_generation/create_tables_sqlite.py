import sqlite3

# Создаем или открываем файл базы данных SQLite
conn = sqlite3.connect('courier_delivery_db.sqlite')  # Файл базы данных будет создан в текущей директории
cursor = conn.cursor()

# Создаем таблицу Role
cursor.execute('''
CREATE TABLE IF NOT EXISTS Role (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
''')

# Создаем таблицу User
cursor.execute('''
CREATE TABLE IF NOT EXISTS User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lastname TEXT,
    name TEXT NOT NULL,
    surname TEXT,
    role_id INTEGER,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    FOREIGN KEY(role_id) REFERENCES Role(id)
);
''')

# Создаем таблицу Order
cursor.execute('''
CREATE TABLE IF NOT EXISTS `Order` (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    address_from_geo_lat REAL,
    address_from_geo_long REAL,
    address_to_geo_lat REAL,
    address_to_geo_long REAL,
    trackers TEXT,
    invoice_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES User(id),
    FOREIGN KEY(invoice_id) REFERENCES Invoice(id)
);
''')

# Создаем таблицу Invoice
cursor.execute('''
CREATE TABLE IF NOT EXISTS Invoice (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    price REAL,
    courier_price REAL,
    commission REAL,
    FOREIGN KEY(order_id) REFERENCES `Order`(id)
);
''')

# Создаем таблицу Tracker
cursor.execute('''
CREATE TABLE IF NOT EXISTS Tracker (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    courier_id INTEGER,
    order_id INTEGER,
    track_number TEXT NOT NULL,
    FOREIGN KEY(courier_id) REFERENCES User(id),
    FOREIGN KEY(order_id) REFERENCES `Order`(id)
);
''')

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()

print("Таблицы успешно созданы!")
