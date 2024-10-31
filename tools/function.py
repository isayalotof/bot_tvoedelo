import sqlite3
from cfg import config as cf


def add_appointment(user_id, service_name, data, day, time_start, comment):
    conn = sqlite3.connect('data.db')  # указываем файл базы данных
    c = conn.cursor()

    # Добавление записи в таблицу
    c.execute("""
            INSERT INTO appointments (user_id, service_name, data, day, time_start, comment)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, service_name, data, day, time_start, comment))

    # Сохранение изменений
    conn.commit()

    # Закрытие соединения
    conn.close()


def get_my_records(user_id):
    conn = sqlite3.connect('data.db')  # указываем файл базы данных
    c = conn.cursor()
    # Выполнение запроса
    c.execute("""SELECT time_start, service_name 
                 FROM appointments 
                 WHERE day = ?""", (user_id,))

    # Получение всех строк результата
    rows = c.fetchall()

    # Преобразование в словарь, где ключом является время, а значением — название услуги
    result = {row[0]: row[1] for row in rows}

    # Вывод или дальнейшая обработка результата
    return result


def get_categories():
    conn = sqlite3.connect('data.db')  # указываем файл базы данных
    c = conn.cursor()
    c.execute("""SELECT name 
                FROM categories 
    """)

    rows = c.fetchall()

    result = {row[0] for row in rows}

    return result


def all_services():
    conn = sqlite3.connect('data.db')  # указываем файл базы данных
    c = conn.cursor()
    c.execute("""SELECT name 
                    FROM services 
        """)
    rows = c.fetchall()

    result = {row[0] for row in rows}

    return result


def get_duration(serv):
    conn = sqlite3.connect('data.db')  # указываем файл базы данных
    c = conn.cursor()
    c.execute("""SELECT duration 
                     FROM services 
                     WHERE name = ?""", (serv,))
    rows = c.fetchall()

    result = {row[0] for row in rows}

    return result


def get_description_of_serv(serv):
    conn = sqlite3.connect('data.db')  # указываем файл базы данных
    c = conn.cursor()
    c.execute("""SELECT description
                     FROM services 
                     WHERE name = ?""", (serv,))
    rows = c.fetchall()

    result = {row[0] for row in rows}

    return result


def is_admin(user_id, __admin_id = cf.admin_id):
    if user_id == __admin_id:
        return True
    return False