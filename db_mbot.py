# import sqlite3
# from datetime import datetime
#
# # Сортировка в просмотре базы
# # https://inloop.github.io/sqlite-viewer/#
# # SELECT * FROM 'messages' ORDER BY date DESC;
#
# # Подключение к базе данных SQLite
# connection = sqlite3.connect("dbase.db")
# cursor = connection.cursor()
#
#
# # Инициализация базы данных: создание таблицы, если её ещё нет
# def initialize_database():
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS messages (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,          -- Уникальный ID записи
#         user_id INTEGER NOT NULL,                      -- ID пользователя Telegram
#         user_name TEXT NOT NULL,                       -- Полное имя пользователя
#         prompt TEXT,                                  -- Запрос пользователя
#         date TEXT NOT NULL,                            -- Дата и время сообщения
#         url_str TEXT,                                 -- URL, связанный с запросом
#         message TEXT,                                 -- Текст сообщения (опционально)
#         interval INTEGER,                             -- Интервал мониторинга (в секундах)
#         url_m3u8 TEXT,                                -- Ссылка для мониторинга
#         scheduler TEXT                                -- Настройки планировщика (опционально)
#     )
#     """)
#     connection.commit()
#
# # Получение следующего порядкового номера сообщения для пользователя (оставляем без изменений)
# def get_user_record_number(user_id: int) -> int:
#     cursor.execute("""
#     SELECT COUNT(*) FROM messages WHERE user_id = ?
#     """, (user_id,))
#     return cursor.fetchone()[0] + 1
#
# # Сохранение сообщения в базу данных
# def save_message(user_id: int, user_name: str, prompt: str = None, url_str : str = None, message_text: str = None, interval: int = None, url_m3u8: str = None, scheduler: str = None):
#     current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#
#     cursor.execute("""
#     INSERT INTO messages (user_id, user_name, prompt, date, url_str, message, interval, url_m3u8, scheduler)
#     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#     """, (user_id, user_name, prompt, current_time, url_str, message_text, interval, url_m3u8, scheduler))
#     connection.commit()