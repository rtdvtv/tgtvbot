import asyncio
import logging
import re
import pytz
from datetime import datetime
from aiogram import types, Router, F
from ai_chat import main_mistral
from status_str import StreamStatusChecker, get_m3u8_info
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import (get_main_menu, get_setup_menu, get_interval_menu, get_admin_menu, get_help_menu,
                       get_sound_menu, get_ai_menu, get_url_str_menu, get_start_key, get_reg_key)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, InlineKeyboardButton
from config import m3u8_url, URL_M3U8
from class_bot import Interval, EchoBotState, Form, InfoState
from sqlalchemy import (create_engine, Column, Integer, String, Text, DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

class Reg(StatesGroup):
    name = State()
    number = State()

router = Router()
stream_checker = StreamStatusChecker(m3u8_url)


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка базы данных SQLite
DATABASE_URL = "sqlite:///dbase.db"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()


# Определение модели таблицы
class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)  # ID пользователя
    username = Column(String(100), nullable=True)  # Имя пользователя
    message_text = Column(Text, nullable=False)  # Текст сообщения
    date = Column(DateTime, nullable=False)  # Дата и время
    url_m3u8 = Column(String(255), nullable=True)  # URL M3U8
    name = Column(String(100), nullable=True)  # Имя URL
    promt = Column(String(255), nullable=True)  # Промт


# Создание таблицы в базе данных
Base.metadata.create_all(engine)

# Создание сессии для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Определение состояний FSM
class Form(StatesGroup):
    url_m3u8 = State()  # Состояние для ввода URL M3U8
    name = State()  # Состояние для ввода имени URL


# Установка часового пояса (Киев)
kiev_tz = pytz.timezone('Europe/Kiev')

# Функция для проверки URL
def is_valid_url(url: str) -> bool:
    """
    Проверяет, начинается ли URL на "http" и заканчивается ли на "m3u8".
    """
    pattern = re.compile(r'^https?://.*\.m3u8$')  # Регулярное выражение для проверки
    return bool(pattern.match(url))

# # ОБРАБОТЧИКИ КОМАНД:
# def register_echo_handlers(dp: router):
#     dp.message.register(cmd_start, Command("start"))
#     dp.message.register(stop_command, F.text == "STOP")
#     # dp.message.register(handle_reg_one, F.text == "REG")
#     dp.message.register(handle_run, F.text == "RUN")
#     dp.message.register(handle_ai_menu, F.text == "AI")
#     dp.message.register(echo_enabled, F.text == "ON")
#     dp.message.register(echo_disabled, F.text == "OFF")
#     dp.message.register(handle_setup, F.text == "SETUP")
#     dp.message.register(process_online_tv, F.text == "ONLINE")
#     dp.message.register(info_command, F.text == "STR_INFO")
#     dp.message.register(handle_interval, F.text == "INTERVAL")
#     dp.message.register(handle_url_str, F.text == "URL_STR")
#     dp.message.register(process_url_set_button, F.text == "URL_SET")
#     dp.message.register(process_list_urls_button, F.text == "URL_LIST")
#     dp.message.register(handle_admin, F.text == "ADMIN")
#     dp.message.register(handle_help, F.text == "HELP")
#     dp.message.register(handle_sound, F.text == "SOUND")
#     dp.message.register(handle_info_command, F.text == "INFO")
#     dp.message.register(handle_check_status, F.text == "CHECK")
#     dp.message.register(command_set_interval, F.text == "SET")
#     # dp.message.register(set_new_interval, StateFilter(IntervalSetting.waiting_for_interval))
#     dp.message.register(handle_go_back, F.text == "BACK")
#     dp.message.register(go_back_from_info, F.text == "MENU")
#     dp.message.register(echo_bot, ~F.text.startswith("/"))  # echo_bot - *после* команд!


# Обработчик кнопки START
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    print("cmd_start:", message.text)
    await message.answer(
        f"Добро пожаловать! {message.from_user.first_name}!\n"
        "Используйте кнопку RUN, чтобы запустить программу.",
        reply_markup=get_start_key())


# # Обработчик кнопки REG
# @router.message(F.text == "REG")
# async def handle_reg_one(message: Message, state: FSMContext):
#     await state.set_state(Reg.name)
#     await message.answer("Введите ваше имя"),


# @router.message(Reg.name)
# async def handle_reg_two(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await state.set.state(Reg.number)
#     await message.answer("Введите ваш номер телефона")
#
#
# @router.message(Reg.number)
# async def handle_reg_three(message: Message, state: FSMContext):
#     await state.update_data(number=message.text)
#     data = await state.get_data()
#     await message.answer((f"Регистрация завершена\n",
#                           f"Имя: {data['name']}\n",
#                           f"Номер: {data['number']}"),
#         reply_markup=get_start_keyboard())
#     await state.clear()


# @router.message(Reg.name)
# def get_send_contact_keyboard():
#     keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
#     contact_button = types.InlineKeyboardButton("Отправить контакт", request_contact=True)
#     keyboard.add(contact_button)
#     return keyboard


# Обработчик кнопки RUN
@router.message(F.text == "RUN")
async def handle_run(message: Message):
    print("handle_run:", message.text)
    green_circle = '\U0001F7E2'
    await message.answer(
        f"{green_circle} Программа инициализирована!\n\n"
        "Для запуска функционала в режиме автоматического мониторинга нажмите на кнопку CHECK. "
        "\n\nПосле обновления статуса потока программа перейдет в автоматический режим.\n"
        "Для ознакомления с функционалом перейдите в меню HELP, для тонкой настройки — в меню SETUP.",
        reply_markup=get_main_menu())


# Обработчик кнопки "BACK"
@router.message(F.text == "BACK")
async def handle_go_back(message: Message):
    await message.answer(
        "Вы перешли в Главное меню",
        reply_markup=get_main_menu())


# # Обработчик кнопки "MENU" для возврата в главное меню и удаление предыдущего сообщения
@router.message(F.text == "MENU")
async def go_back_from_info(message: types.Message, state: FSMContext):
    data = await state.get_data()
    description_message_id = data.get("description_message_id")
    if description_message_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=description_message_id)
        except Exception as e:
            print(f"Ошибка при удалении сообщения: {e}")
        await state.update_data(description_message_id=None)  # Сбрасываем message_id
    await message.delete()  # Удаляем сообщение с кнопкой MENU
    await message.answer("Вы вернулись в главное меню", reply_markup=get_main_menu())


# Обработчик кнопки SETUP
@router.message(F.text == "SETUP")
async def handle_setup(message: Message):
    await message.answer(
        "Раздел SETUP. \nВыберите нужный пункт:",
        reply_markup=get_setup_menu())


# Обработчик кнопки INTERVAL
@router.message(F.text == "INTERVAL")
async def handle_interval(message: Message):
    await message.answer(
        "HANDLERS - handle_interval\n"
        "Устанавливаем интервал запроса статуса потока"
        "в фоновом режиме (не менее 60 секунд)\n"
        "Введите время в секундах:",
        reply_markup=get_interval_menu())


# # Обработчик кнопки URL_STR
@router.message(lambda message: message.text == "URL_STR")
async def handle_url_str(message: types.Message):
    await message.answer(
        "Добро пожаловать! Используйте кнопки для управления.",
        reply_markup=get_url_str_menu())


# # Получаем текст сообщения
#     text_to_save = message.text

    # # Проверяем, что message.from_user не None
    # if message.from_user is None:
    #     await message.answer("Ошибка: не удалось получить данные пользователя.")
    #     return
    #
    # # Сохраняем текст в базу данных
    # new_message = Message(message_text=text_to_save)
    # session.add(new_message)
    # session.commit()



# Обработчик кнопки "URL_SET"
@router.message(lambda message: message.text == "URL_SET")
async def process_url_set_button(message: types.Message, state: FSMContext):
    # Запрашиваем URL M3U8
    await message.answer("Пожалуйста, введите URL M3U8 (должен начинаться на 'http' и заканчиваться на 'm3u8'):")
    # Устанавливаем состояние для ожидания ввода URL M3U8
    await state.set_state(Form.url_m3u8)


# Обработчик для ввода URL M3U8
@router.message(Form.url_m3u8)
async def process_url_m3u8(message: types.Message, state: FSMContext):
    url_m3u8 = message.text  # URL M3U8, введенный пользователем

    # Проверяем URL
    if not is_valid_url(url_m3u8):
        await message.answer(
            "Некорректный URL. Пожалуйста, введите URL, который начинается на 'http' и заканчивается на 'm3u8'.")
        return  # Не сбрасываем состояние, чтобы пользователь мог ввести URL заново

    # Проверяем, существует ли URL уже в базе данных
    existing_url = session.query(Message).filter(Message.url_m3u8 == url_m3u8).first()
    if existing_url:
        await message.answer("Этот URL уже существует в списке.")
        await state.clear()
        return

    # Сохраняем URL в состояние
    await state.update_data(url_m3u8=url_m3u8)

    # Запрашиваем имя для URL
    await message.answer("Пожалуйста, введите имя для этого URL:")
    await state.set_state(Form.name)


# Обработчик для ввода имени URL
@router.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text  # Имя, введенное пользователем
    data = await state.get_data()  # Получаем сохраненный URL
    url_m3u8 = data.get("url_m3u8")

    # Собираем данные
    user_id = message.from_user.id
    username = message.from_user.username
    message_text = "URL_SET"  # Текст кнопки
    date = datetime.now(kiev_tz)  # Устанавливаем время в часовом поясе Киев
    promt = "Ввод пользователя"  # Пример промта (можно заменить на ввод от пользователя)

    try:
        # Сохраняем данные в базу данных
        new_message = Message(
            user_id=user_id,
            username=username,
            message_text=message_text,
            date=date,
            url_m3u8=url_m3u8,
            name=name,
            promt=promt
        )
        session.add(new_message)
        session.commit()

        # Логируем успешное сохранение
        logger.info(f"Данные сохранены в базу данных: {new_message}")

        # Отправляем подтверждение пользователю
        green_circle = '\U0001F7E2'
        await message.answer(
            f"{green_circle} Данные успешно сохранены:\n"
            f"ID: {new_message.id}\n"
            f"User ID: {new_message.user_id}\n"
            f"Username: {new_message.username}\n"
            f"Текст сообщения: {new_message.message_text}\n"
            f"Дата: {new_message.date}\n"
            f"URL M3U8: {new_message.url_m3u8}\n"
            f"Имя: {new_message.name}\n"
            f"Промт: {new_message.promt}"
        )
    except SQLAlchemyError as e:
        # Логируем ошибку
        logger.error(f"Ошибка при сохранении данных в базу данных: {e}")
        await message.answer("Произошла ошибка при сохранении данных. Пожалуйста, попробуйте позже.")
    finally:
        # Сбрасываем состояние
        await state.clear()


# Обработчик кнопки "Список URL"
@router.message(lambda message: message.text == "URL_LIST")
async def process_list_urls_button(message: types.Message, state: FSMContext):

    # Сбрасываем состояние, если оно было активно
    current_state = await state.get_state()
    if current_state:
        await state.clear()

    # Получаем все URL из базы данных
    urls = session.query(Message).all()

    if not urls:
        await message.answer("Список URL пуст.")
        return

    # Формируем текстовый список URL с порядковыми номерами и именами
    url_list = "\n".join(
        [f"{i + 1}. {url.name} - {url.url_m3u8} ({url.date.astimezone(kiev_tz).strftime('%Y-%m-%d %H:%M:%S')})" for
         i, url in enumerate(urls)])

    # Формируем inline-кнопки для удаления и просмотра
    builder = InlineKeyboardBuilder()
    for i, url in enumerate(urls):
        # Добавляем кнопки "Del" и "View" для каждого URL в одну строку
        builder.row(
            InlineKeyboardButton(text=f"Del {i + 1}", callback_data=f"delete_{url.id}"),
            InlineKeyboardButton(text=f"View {i + 1}", callback_data=f"watch_{url.id}")
        )

    # Отправляем сообщение с нумерованным списком URL и кнопками
    await message.answer(
        f"Список URL:\n{url_list}",
        reply_markup=builder.as_markup()
    )


# Обработчик для удаления URL через inline-кнопку
@router.callback_query(lambda c: c.data.startswith("delete_"))
async def process_delete_url(callback: types.CallbackQuery):
    url_id = int(callback.data.split("_")[1])  # Получаем ID URL из callback_data
    url = session.query(Message).filter(Message.id == url_id).first()

    if url:
        session.delete(url)
        session.commit()
        await callback.message.answer(f"URL с ID {url_id} успешно удален.")
    else:
        await callback.message.answer(f"URL с ID {url_id} не найден.")

    # Обновляем список URL
    await process_list_urls_button(callback.message)


# Обработчик для просмотра URL через inline-кнопку
@router.callback_query(lambda c: c.data.startswith("watch_"))
async def process_watch_url(callback: types.CallbackQuery):
    # Получаем ID URL из callback_data
    url_id = int(callback.data.split("_")[1])

    # Ищем URL в базе данных
    url = session.query(Message).filter(Message.id == url_id).first()

    if url:
        # Отправляем пользователю ссылку для просмотра
        await callback.message.answer(f"Смотрите ONLINE-TV: {url.url_m3u8}")
    else:
        # Если URL не найден, отправляем сообщение об ошибке
        await callback.message.answer("URL не найден.")


# Обработчик кнопки "ONLINE_TV"
@router.message(lambda message: message.text == "ONLINE_TV")
async def process_online_tv(message: types.Message, state: FSMContext):
    # Сбрасываем состояние, если оно было активно
    current_state = await state.get_state()
    if current_state:
        await state.clear()  # Сбрасываем состояние

    # Получаем последний добавленный URL
    last_url = session.query(Message).order_by(Message.id.desc()).first()

    if not last_url:
        await message.answer("Нет доступных URL для просмотра.")
        return

    # Отправляем ссылку для просмотра
    await message.answer(f"Смотрите ONLINE-TV: {last_url.url_m3u8}")


# Обработчик кнопки "ADMIN"
@router.message(F.text == "ADMIN")
async def handle_admin(message: Message):
    await message.answer(
        "Раздел ADMIN. \nВыберите нужный пункт:",
        reply_markup=get_admin_menu())


# Обработчик кнопки "HELP"
@router.message(F.text == "HELP")
async def handle_help(message: Message):
    await message.answer(
        "Раздел HELP. \nВыберите нужный пункт:",
        reply_markup=get_help_menu())


# Обработчик кнопки "SOUND"
@router.message(F.text == "SOUND")
async def handle_sound(message: Message):
    await message.answer(
        "Раздел SOUND. \nВыберите нужный пункт:",
        reply_markup=get_sound_menu())


# Обработчик кнопки "INFO"
# @router.message(F.text == "INFO")
# async def handle_info(message: Message):
#     await message.answer(
#         "Раздел INFO. \nВыберите нужный пункт:",
#         reply_markup=get_info_menu())


# Обработчик кнопки "INFO" из главного меню (открывает инлайн кнопки/в about_bot.py)
@router.message(F.text == "INFO")
async def handle_info_command(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="RU", callback_data="ru_info")
    builder.button(text="EN", callback_data="en_info")
    await message.answer("Описание функционала бота:",
        # await message.delete(),  # Удаляем сообщение с описанием
                         reply_markup=builder.as_markup())


# # обработчики для инлайн-кнопок RU и EN
# @router.callback_query(F.data == "ru_info")
# async def ru_info(callback: types.CallbackQuery, state: FSMContext):
#     description = """
# Telegram-бот "RTDVTV Monitor" — это профессиональное решение для мониторинга потоков в формате M3U8.
# Бот разработан для пользователей, которым необходимо отслеживать статус потоков,
# получать уведомления об изменениях статуса потока. Создавать и управлять списком ссылок для мониторинга.
#
# Основные функции бота:
# Мониторинг потоков:
#     - Бот постоянно проверяет статус потока после запуска команды RUN или нажатия кнопки CHECK.
#     - В фоновом режиме бот отслеживает доступность потока и уведомляет пользователя о его статусе (**ONLINE**/**OFFLINE**).
#     - Пользователь может просматривать параметры потока, такие как битрейт и размер изображения.
#
# Управление списком потоков:
#     - Бот позволяет добавлять, удалять и просматривать ссылки на потоки.
#     - Пользователь может выбрать конкретную ссылку для мониторинга или просмотра в режиме реального времени.
#     - Поддерживается возможность редактирования списка ссылок через интерактивное меню.
#
# Встроенный текстовый ИИ (Ai-Mistral):
#     - Бот оснащен текстовым ИИ с функцией контекста, который можно активировать или деактивировать по команде.
#     - Бот позволяет работать с ИИ не прерывая процесс мониторинга.
#
# Планировщик событий (SCHEDULER):
#     - Бот поддерживает создание напоминаний и автоматическое добавление ссылок для мониторинга в установленное время автоматическом режиме.
#     - Пользователь может настроить уведомления о событиях, которые будут отправляться в указанное время.
#
# Уведомления и рассылка:
#     - Бот отправляет уведомления об изменениях статуса потока.
#     - Пользователь может настроить отправку уведомлений отдельным пользователям.
#
# Интерактивное меню:
#     - Бот оснащен удобным меню с кнопками для быстрого доступа к основным функциям.
#     - Пользователь может легко переключаться между разделами: мониторинг, настройки, ИИ, планировщик и т.д.
#     - Меню адаптировано для использования как на мобильных устройствах, так и на компьютерах.
#
# Автоматизация мониторинга:
#     - **Автоматизация:** Бот работает в фоновом и ручном режимах.
#     - Гибкость:** Возможность добавлять и управлять списком потоков, а также настраивать уведомления.
#     - Интеграция ИИ:** Встроенный текстовый ИИ расширяет функционал бота, делая его универсальным инструментом.
#     - Простота использования:** Интуитивно понятное меню и команды делают бота доступным для пользователей любого уровня подготовки.
#
# Пример использования:
#     1. Пользователь запускает бота командой **/start**.
#     2. Добавляет ссылку на поток через меню **URL_STR**.
#     3. Запускает мониторинг командой **RUN**.
#     4. Получает уведомления о статусе потока (ONLINE/OFFLINE).
#     5. При запросе "STR_INFO" получает параметры потока.
#     6. Использует текстовый ИИ для получения дополнительной информации.
#     7. Настраивает планировщик для автоматического мониторинга в определенное время.
#
# <b>Технические особенности</b>:
#     - Язык программирования и библиотеки:Python/ Aiogram/ SQLite
#     - Библиотеки:** Aiogram, Sqlalchemy, m3u8, Asyncio, FsmStorage.
#     - База данных:** SQLite.
#     - Интеграция: Поддержка Telegram API, текстовый ИИ на базе Mistral
#
#     **Created by "RTDVTV"** (rtdvtv@gmail.com)
#     """
#
#     message = await callback.message.answer(description)
#     await state.update_data(description_message_id=message.message_id)
#     await callback.answer()
#
#
#     # await callback.message.answer(description)
#     # await callback.answer()  # Убираем индикатор загрузки
#     await callback.message.edit_reply_markup(reply_markup=None) # Удаляем инлайн клавиатуру
#
# @router.callback_query(F.data == "en_info")
# async def en_info(callback: types.CallbackQuery, state: FSMContext):
#     description = """
# The Telegram bot "RTDVTV Monitor" is a professional solution for monitoring M3U8 streams.
# Designed for users who need to track stream statuses, receive notifications about changes, a
# nd manage a list of links for monitoring, the bot also features a built-in text AI and an event scheduler,
# making it a versatile tool for working with media streams.
#
# Key Features of the Bot
#
# Stream Monitoring:
#     - The bot continuously checks the stream status after the **RUN** command is executed or the **CHECK** button is pressed.
#     - In the background, the bot monitors stream availability and notifies the user of its status (ONLINE/OFFLINE).
#     - Users can view stream parameters such as bitrate and image size.
#
# Stream List Management:
#     - The bot allows users to add, delete, and view stream links.
#     - Users can select a specific link for monitoring or real-time viewing.
#     - The bot supports editing the list of links through an interactive menu.
#
# Built-in Text AI:
#    - The bot is equipped with a text AI that can be activated or deactivated on command.
#    - The AI enables users to ask questions and receive answers without interrupting the stream monitoring process.
#
# Event Scheduler:
#     - The bot supports creating reminders and automatically adding links for monitoring at specified times.
#     - Users can configure event notifications to be sent at designated times.
#     - The scheduler allows for flexible task management and automation of routine processes.
#
# Notifications and Broadcasting:
#     - The bot sends notifications about stream status changes.
#     - Users can configure notifications to be sent to specific users or groups.
#     - Notifications can be personalized based on user preferences.
#
# Interactive Menu:
#     - The bot features a user-friendly menu with buttons for quick access to core functions.
#     - Users can easily switch between sections: monitoring, settings, AI, scheduler, etc.
#     - The menu is optimized for use on both mobile devices and computers.
#
# Advantages of the Bot:
#     - Automation of Monitoring:** The bot operates in the background, allowing users to focus on other tasks.
#     - Flexibility:** Users can add and manage a list of streams and customize notifications.
#     - AI Integration:** The built-in text AI enhances the bot's functionality, making it a versatile tool.
#     - Ease of Use:** An intuitive menu and commands make the bot accessible to users of all skill levels.
#     - Reliability:** The bot utilizes modern technologies to ensure stable operation and accuracy for software or visual monitoring.
#
# Example of Use
# 1. The user starts the bot with the **/start** command.
# 2. Adds a stream link via the **URL_STR** menu.
# 3. Initiates monitoring with the **RUN** command.
# 4. Receives notifications about the stream status (ONLINE/OFFLINE).
# 5. Requests "STR_INFO" to obtain stream parameters.
# 6. Uses the text AI to get additional information.
# 7. Configures the scheduler for automatic monitoring at specified times.
#
# Technical Specifications:
# - **Programming Language:** Python
# - **Libraries:** aiogram, sqlalchemy, m3u8, asyncio
# - **Database:** SQLite for storing user data, stream lists, and user settings.
# - **Integration:** Telegram API support, text AI based on Mistral.
#
# Created by "RTDVTV" (rtdvtv@gmail.com)
#     """
#
#     message = await callback.message.answer(description)
#     await state.update_data(description_message_id=message.message_id)
#     await callback.answer()
#
#     # await callback.message.answer(description)
#     # await callback.answer()  # Убираем индикатор загрузки
#     await callback.message.edit_reply_markup(reply_markup=None) # Удаляем инлайн клавиатуру




# AI - обработка кнопки с подменю
@router.message(F.text == "AI")
async def handle_ai_menu(message: Message):
    yellow_circle = '\U0001F7E0'  # Зеленый кружок
    await message.answer(
        f"{yellow_circle} Для запуска 'AiChat' нажмите кнопку 'ON'."
        "\n\nТеперь вы можете использовать строку для ввода запросов в чат.\n"
        "Для завершения работы 'AiChat' и перехода в режим мониторинга"
        " нажмите кнопку 'OFF', затем 'BACK' для возврата функционала."
        "\n\nВо время использования чата, мониторинг работает в фоне и при изменении статуса"
        " потока выведет соответствующее уведомление не смотря на работу 'AiChat'.",
        reply_markup=get_ai_menu())


# Обработчик кнопки CHECK
@router.message(F.text == "CHECK")
async def handle_check_status(message: Message):
    status = await stream_checker.check_stream_status()
    if status:
        yellow_triangle = '\U0001F7E1'
        await message.answer(f"{yellow_triangle} Обновление")
        await asyncio.sleep(2)
        green_circle = '\U0001F7E2'
        await message.answer(f"{green_circle} Check-Status: ONLINE")
    else:
        red_circle = '\U0001F534'
        await message.answer(f"{red_circle} Check-Status: OFFLINE")
        print("Def Check_status")


# Функция для вызова информации о потоке. На прямую из главного меню по кнопке INFO
@router.message(F.text == "STR_INFO")
async def info_command(message: types.Message):
    info = get_m3u8_info(URL_M3U8)  # Получаем информацию о потоке
    if info:
        bitrate_mbps = info['bitrate'] / 1_000_000 if info['bitrate'] else 0  # Преобразуем битрейт в Мбит/с
        await message.answer(f"Битрейт: {bitrate_mbps:.2f} Мбит/с\nРазрешение: {info['resolution']}")
    else:
                await message.answer("Не удалось получить информацию о потоке.")
    arrow_down = '\U00002B07'
    await message.answer(f"{arrow_down}", reply_markup=get_main_menu())  # Возвращаемся в главное меню


# Функции для работы с интервалом (INTERVAL->(SET/SHOW))
@router.message(Command("set_interval"))
async def command_set_interval(message: Message, state: FSMContext) -> None:
    await message.answer("Пожалуйста, введите только числовое значение"),
    await state.set_state(Interval.time)


@router.message(Interval.time)
async def set_new_interval(message: Message, state: FSMContext) -> None:
    try:
        time = int(message.text)  # Получаем message.text *внутри* функции
        if time < 60:
            await message.reply("Интервал не может быть меньше 60 секунд.")
            return

        await state.update_data(time=time)
        current_state = await state.get_state()
        await message.answer(f"Интервал обновлен: {current_state} секунд.")
        await state.clear()
        print(set_new_interval)

    except ValueError:
        await message.reply("Пожалуйста, введите только числовое значение")
        return

    except Exception as e:
        logging.error(f"Ошибка при установке интервала: {e}")
        await message.reply("Произошла ошибка при установке интервала. Попробуйте еще раз.")
        return


# Обработчик кнопки "ON" для запуска "AI"
@router.message(Command("ON"))
async def echo_enabled(message: types.Message, state: FSMContext):
    await state.set_state(EchoBotState.enabled)
    green_circle = '\U0001F7E2'
    await message.reply(f"{green_circle} AiChat включен.")


# Обработчик кнопки "OFF" для остановки "AI"
@router.message(Command("OFF"))
async def echo_disabled(message: types.Message, state: FSMContext):
    await state.set_state(EchoBotState.disabled)
    red_circle = '\U0001F534'
    await message.reply(f"{red_circle} AiChat выключен.")
    await message.answer(  # Переход в главное меню
        "Вы перешли в Главное меню",
        reply_markup=get_main_menu()
    )

# Обработчик команд которые начинаются с "/" чтобы не попадали в эхобот
@router.message(~F.text.startswith("/"))
async def echo_bot(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == EchoBotState.enabled.state:
        try:
            content = message.text
            res = await main_mistral(content)
            await message.answer(res)
        except TypeError:
            await message.reply(message.text)

# Обработчик команды /stop
# @router.message(Command("stop"))
# async def stop_command(message: types.Message):
#     stream_checker.stop_monitoring()
#     red_circle = '\U0001F534'
#     await message.answer(f"{red_circle} Мониторинг остановлен.")

@router.message(lambda message: message.text == "STOP")
async def stop_command(message: types.Message):
    stream_checker.stop_monitoring()
    red_circle = '\U0001F534'
    await message.answer(f"{red_circle} Мониторинг остановлен.")