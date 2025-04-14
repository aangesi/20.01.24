from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Подключение к базе данных
def get_db_connection():
    conn = sqlite3.connect('courier_delivery_db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM full_info').fetchall()
    conn.close()
    return render_template('index.html', data=data)

@app.route('/filter', methods=['GET'])
def filter_data():
    filters = request.args
    query = "SELECT * FROM full_info WHERE 1=1"
    params = []

    # Применяем фильтрацию по отдельным полям с использованием LIKE
    if 'user_nickname' in filters and filters['user_nickname']:
        query += " AND user_nickname LIKE ?"
        params.append(f"%{filters['user_nickname']}%")
    if 'address_from' in filters and filters['address_from']:
        query += " AND address_from LIKE ?"
        params.append(f"%{filters['address_from']}%")
    if 'address_to' in filters and filters['address_to']:
        query += " AND address_to LIKE ?"
        params.append(f"%{filters['address_to']}%")
    if 'track_number' in filters and filters['track_number']:
        query += " AND track_number LIKE ?"
        params.append(f"%{filters['track_number']}%")
    if 'invoice_price' in filters and filters['invoice_price']:
        query += " AND invoice_price LIKE ?"
        params.append(f"%{filters['invoice_price']}%")  # Изменил на LIKE для поиска по цене
    if 'courier_price' in filters and filters['courier_price']:
        query += " AND courier_price LIKE ?"
        params.append(f"%{filters['courier_price']}%")  # То же для courier_price
    if 'commission' in filters and filters['commission']:
        query += " AND commission LIKE ?"
        params.append(f"%{filters['commission']}%")  # И для commission

    conn = get_db_connection()
    data = conn.execute(query, params).fetchall()
    conn.close()

    return jsonify([dict(row) for row in data])

if __name__ == '__main__':
    app.run(debug=True)
