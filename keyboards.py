from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types, Dispatcher


# РАЗДЕЛ МЕНЮ: #####################################################

# ГЛАВНОЕ МЕНЮ
def get_main_menu():
    return ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="CHECK"),  # Первая строка
            KeyboardButton(text="ONLINE"),
            KeyboardButton(text="STOP")],
        [KeyboardButton(text="SETUP"),  # Вторая строка
            KeyboardButton(text="STR_INFO"),
            KeyboardButton(text="HELP")]
    ], resize_keyboard=True,
    input_field_placeholder = "Выберите пункт меню")


# Создание клавиатуры Подменю для кнопки "SETUP"
def get_setup_menu():
    return ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="INTERVAL"),  KeyboardButton(text="URL_STR"),
            KeyboardButton(text="SOUND")],
        [KeyboardButton(text="ADMIN"), KeyboardButton(text="BACK")]],
        resize_keyboard=True)


# Создание клавиатуры Подменю для кнопки "INTERVAL"
def get_interval_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="SET"), KeyboardButton(text="SHOW"), KeyboardButton(text="BACK")]],
        resize_keyboard=True)


# Подменю для кнопки "URL_STR"
# def get_url_str_menu():
#     return ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text="URL_SET"),KeyboardButton(text="URL_LIST"), KeyboardButton(text="URL_DEL")],
#             [KeyboardButton(text="LOG"), KeyboardButton(text="BACK")]],    # Вторая строка: кнопка BACK
#         resize_keyboard=True)

def get_url_str_menu():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="URL_SET"))
    builder.add(KeyboardButton(text="URL_LIST"))
    builder.add(KeyboardButton(text="BACK"))
    builder.add(KeyboardButton(text="ONLINE"))
    return builder.as_markup(resize_keyboard=True)

# Создание клавиатуры Подменю для кнопки "ADMIN"
def get_admin_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="BUT1"), KeyboardButton(text="BUT2"), KeyboardButton(text="BUT3")],
            [KeyboardButton(text="SUPPOR"), KeyboardButton(text="BACK")]], # Вторая строка: кнопка BACK
        resize_keyboard=True)

# Cоздание клавиатуры Подменю для кнопки "HELP"
def get_help_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="SCHEDULER"), KeyboardButton(text="COMMAND"), KeyboardButton(text="INFO")],
            [KeyboardButton(text="AI"), KeyboardButton(text="MENU")]],  # Вторая строка: кнопка BACK
            resize_keyboard=True)


# Создание клавиатуры Подменю для кнопки "AI"
def get_ai_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="ON"), KeyboardButton(text="OFF"), KeyboardButton(text="BACK")]],  # Кнопка OFF это стоп для ИИ и выход в меню
            resize_keyboard=True)

# Создание клавиатуры Подменю для кнопки "SOUND"
def get_sound_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="SILENT"), KeyboardButton(text="SPEAKER"), KeyboardButton(text="BACK")]],
            resize_keyboard=True)


# # Создание кнопки "MENU" как подменю для кнопки "INFO"
# def get_info_menu():
#     return ReplyKeyboardMarkup(
#     keyboard=[KeyboardButton(text="MENU")],
#     resize_keyboard=True)  # кнопка для вызова ответного сообщения с описанием программы и контактов автора

# Создание клавиатуры Подменю для кнопки "STR-INFO"
def get_str_info_menu():
    return ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="STR_INFO"), KeyboardButton(text="BACK")]],
    resize_keyboard=True)  # кнопка для вызова ответного сообщения с описанием параметров потока

# Создание клавиатуры Подменю для кнопки "SET"
def get_set_interval_menu():
    return ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="SET"), KeyboardButton(text="BACK")]],
    resize_keyboard=True)  # кнопка для ввода временного интервала для мониторинга потока

# Создание клавиатуры Подменю для кнопки "SHOW"
def get_show_interval_menu():
    return ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="SHOW"), KeyboardButton(text="BACK")]],
    resize_keyboard=True)  # кнопка для просмотра установленного интервала времени обращений для мониторинга потока



# РАЗДЕЛ КНОПКИ ###################################################

# Создание клавиатуры для кнопки "REG"
def get_reg_key():
    return ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="REG")]], # Одна кнопка в строке после команды START
    resize_keyboard=True,
    one_time_keyboard=True)

# Создание клавиатуры для кнопки "RUN"
def get_start_key():
    return ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="RUN")]], # Одна кнопка в строке после команды START
    resize_keyboard=True)

# Создание клавиатуры для кнопки "CHECK"
def get_check_key():
    return ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="CHECK")]], # Кнопка в главном меню
    resize_keyboard=True)

# Создание клавиатуры для кнопки "BACK"
def get_go_back_key():
    return ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="BACK")]], # Одна кнопка из каждого подменю возврат в Главное меню
    resize_keyboard=True)


# "STOP" Клавиатура с начальной кнопкой
# def get_go_back():
#     return ReplyKeyboardMarkup(
#     keyboard=[[KeyboardButton(text="STOP")]], # Кнопка в главном меню
#     resize_keyboard=True)