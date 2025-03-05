from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Разрешает запросы с других источников (CORS)

# Функция для подключения к базе данных SQLite
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # Позволяет возвращать строки как словари
    return conn

# Создание таблицы Users
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            FIO TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"message": "Привет из Flask!", "items": [1, 2, 3, 4, 0]}
    return jsonify(data)

@app.route('/api/users', methods=['POST'])
def create_user():
    new_user = request.get_json()
    username = new_user.get('username')
    password = new_user.get('password')
    FIO = new_user.get('FIO')
    phone = new_user.get('phone')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Users (username, password, FIO, phone)
        VALUES (?, ?, ?, ?)
    ''', (username, password, FIO, phone))
    conn.commit()
    conn.close()

    return jsonify({"message": "Пользователь создан!"}), 201

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()
    conn.close()

    return jsonify([dict(user) for user in users])

if __name__ == '__main__':
    create_table()  # Создаем таблицу при запуске приложения
    app.run(debug=True, port=5000)