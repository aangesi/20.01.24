from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, send
import sqlite3

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Подключение к БД
def get_db_connection():
    conn = sqlite3.connect('chat.db')
    conn.row_factory = sqlite3.Row
    return conn

# Создание таблиц
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            FIO TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def chat():
    return render_template('sj.html')

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username, password, fio, phone = data['username'], data['password'], data['FIO'], data['phone']

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO Users (username, password, FIO, phone) VALUES (?, ?, ?, ?)',
                       (username, password, fio, phone))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 400
    finally:
        conn.close()

    return jsonify({"message": "User created"}), 201

@app.route('/api/messages', methods=['GET'])
def get_messages():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Messages ORDER BY timestamp DESC LIMIT 20')
    messages = cursor.fetchall()
    conn.close()

    return jsonify([dict(msg) for msg in messages])

@socketio.on('message')
def handle_message(data):
    username, message = data['username'], data['message']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Messages (username, message) VALUES (?, ?)', (username, message))
    conn.commit()
    conn.close()

    send({"username": username, "message": message}, broadcast=True)

if __name__ == '__main__':
    create_tables()
    socketio.run(app, debug=True, port=5000)