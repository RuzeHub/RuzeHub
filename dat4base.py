#database
import sqlite3

# Создаем подключение к базе данных (если её нет — она создастся)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Создаем таблицу (если её нет)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")
conn.commit()

# Функция проверки логина и пароля
def check_user(login, password):
    cursor.execute("SELECT * FROM users WHERE login = ? AND password = ?", (login, password))
    return cursor.fetchone() is not None

# Основной код
login = input("Login: ")
password = input("Password: ")
secret_command = input("Введите '--d' для просмотра последнего пользователя: ")

if secret_command == "--d":
    # Получаем последнего пользователя из БД
    cursor.execute("SELECT login, password FROM users ORDER BY id DESC LIMIT 1")
    last_user = cursor.fetchone()
    if last_user:
        print(f"Последний пользователь: Login = {last_user[0]}, Password = {last_user[1]}")
    else:
        print("В базе данных нет пользователей!")
else:
    # Проверяем введенные данные
    if check_user(login, password):
        print("✅ Вход выполнен!")
        # Добавляем пользователя в БД (если его нет)
        cursor.execute("INSERT OR IGNORE INTO users (login, password) VALUES (?, ?)", (login, password))
        conn.commit()
    else:
        print("❌ Неверный логин или пароль!")

conn.close()
