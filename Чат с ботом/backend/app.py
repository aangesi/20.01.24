from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import base64
import sqlite3
from datetime import datetime
import re
import requests
import json
# ==== Настройка Flask и SocketIO ====
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
API_KEY="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"
# ==== Пользователи по SID ====
users = {}




def get_bot(message):
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    data=json.dumps({
        "model": "shisa-ai/shisa-v2-llama3.3-70b:free",
        "messages": [
            {
                "role": "system",
                "content": "Отвечай всегда на русском"
            },
        {
            "role": "user",
            "content": message
        }
        ],
        
    })
    )
    answer = json.loads(response.text)
    print(answer)
    return answer["choices"][0]["message"]["content"]
# ==== Настройка базы данных ====
DB_NAME = "chat.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT,
            image TEXT,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_message(username, message=None, image=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO messages (username, message, image, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (username, message, image, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

# ==== Инициализация базы ====
init_db()

# ==== Список запрещённых слов ====
BAD_WORDS = {"дурак", "идиот", "черт", "блин"}

def filter_bad_words(message):
    words = message.split()
    filtered = []
    for word in words:
        clean_word = re.sub(r'[^\w]', '', word.lower())
        if clean_word in BAD_WORDS:
            filtered.append("*" * len(word))
        else:
            filtered.append(word)
    return " ".join(filtered)

# ==== Настройки и логика бота ====
BOT_NAME = "бот"

def get_bot_response(message):
    message_lower = message.lower()
    return get_bot(message_lower)

# ==== WebSocket события ====

@socketio.on("connect")
def handle_connect():
    print("Пользователь подключился")

@socketio.on("join")
def handle_join(username):
    users[request.sid] = username
    emit("user_joined", {"username": username}, broadcast=True)

@socketio.on("message")
def handle_message(data):
    username = users.get(request.sid, "Unknown")
    message = data.get("message", "").strip()

    if not message:
        return

    # Фильтрация мата
    clean_message = filter_bad_words(message)

    # Проверка на вызов бота
    if clean_message.lower().startswith(f"@{BOT_NAME}"):
        user_text = clean_message[len(BOT_NAME) + 2:].strip()
        bot_reply = get_bot_response(user_text)
        save_message(BOT_NAME, message=bot_reply)
        emit("message", {"username": BOT_NAME, "message": bot_reply}, broadcast=True)
    else:
        save_message(username, message=clean_message)
        emit("message", {"username": username, "message": clean_message}, broadcast=True)

@socketio.on("image")
def handle_image(data):
    username = users.get(request.sid, "Unknown")
    image_data = data.get("image", "")

    if image_data:
        save_message(username, image=image_data)
        emit("image", {"username": username, "image": image_data}, broadcast=True)

@socketio.on("disconnect")
def handle_disconnect():
    if request.sid in users:
        username = users.pop(request.sid)
        emit("user_left", {"username": username}, broadcast=True)

# ==== HTTP API для получения истории чата ====

@app.route("/messages", methods=["GET"])
def get_messages():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT username, message, image, timestamp FROM messages ORDER BY id ASC")
    messages = [
        {"username": row[0], "message": row[1], "image": row[2], "timestamp": row[3]}
        for row in c.fetchall()
    ]
    conn.close()
    return jsonify(messages)

# ==== Запуск сервера ====
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
