import sqlite3

from datetime import datetime


def init_db():
    """Инициализация базы данных."""
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_address TEXT,
            message TEXT,
            received_at TEXT
        )
    ''')
    conn.commit()
    return conn


# Функция для добавления записи в базу данных
def log_message_to_db(conn, client_address, message):
    """Добавление записи в базу данных."""
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (client_address, message, received_at)
        VALUES (?, ?, ?)
    ''', (
        client_address,
        message,
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ))
    conn.commit()
