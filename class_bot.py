from aiogram.fsm.state import State, StatesGroup

class EchoBotState(StatesGroup): # Создаем класс состояний для эхо-бота
    enabled = State() # Состояние "включен"
    disabled = State() # Состояние "выключен"

# Состояния FSM
class IntervalSetting(StatesGroup):
    waiting_for_interval = State()  # Состояние ожидания

#  Класс для ввода интервала времени INTERVAL
class Interval(StatesGroup):
    time = State()
    # waiting_for_interval = State()

#  Класс для удаления сообщения с инлайн кнопок INRO (RU/EN)
class InfoState(StatesGroup):
    description_message_id = State()

#  Класс для регистрации пользователя
class Reg(StatesGroup):
    name = State()
    number = State()
    company = State()
    email = State()

# Определение состояний FSM
class Form(StatesGroup):
    url_m3u8 = State()  # Состояние для ввода URL M3U8
    name = State()  # Состояние для ввода имени URL

