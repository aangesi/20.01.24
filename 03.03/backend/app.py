from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate  # Import Migrate

app = Flask(__name__)

# Настройка базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Инициализация Bcrypt для хеширования паролей
bcrypt = Bcrypt(app)

# Включаем CORS для всех запросов
CORS(app)

# Инициализация Flask-Migrate
migrate = Migrate(app, db)

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    FIO = db.Column(db.String(200), nullable=True)  # Может быть пустым
    phone = db.Column(db.String(20), nullable=True)  # Может быть пустым

    def __repr__(self):
        return f'<User {self.username}>'

# Функция для хеширования пароля
def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

# Функция для проверки пароля
def check_password(hashed_password, password):
    return bcrypt.check_password_hash(hashed_password, password)

# Эндпоинт для добавления нового пользователя
@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()

    # Получаем данные из запроса
    username = data.get('username')
    password = data.get('password')
    FIO = data.get('FIO', '')  # Если нет, то пустая строка
    phone = data.get('phone', '')  # Если нет, то пустая строка

    # Проверка на наличие обязательных полей
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # Проверка, существует ли уже пользователь с таким именем
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    # Хешируем пароль
    hashed_password = hash_password(password)

    # Создаем нового пользователя
    new_user = User(username=username, password=hashed_password, FIO=FIO, phone=phone)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating user', 'error': str(e)}), 500

# Запуск приложения
if __name__ == '__main__':
    # Создаем таблицы в базе данных, если они еще не существуют
    with app.app_context():
        db.create_all()

    # Запускаем сервер
    app.run(debug=True)
