from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup


# # Состояние для установки URL
# class UrlSetting(StatesGroup):
#     waiting_for_url = State()


# async def set_url_handler(message: types.Message, state: FSMContext):
#     await message.answer("Введите новый URL:")
#     await state.set_state(UrlSetting.waiting_for_url)
#
# async def save_url_handler(message: types.Message, state: FSMContext, user_id, save_m3u8_url, stream_checker):
#     url = message.text
#     if save_m3u8_url(user_id, url):
#         global m3u8_url  # Объявляем m3u8_url как глобальную переменную
#         m3u8_url = url  # Присваиваем ей новое значение
#         stream_checker.m3u8_url = url  # Изменяем url в экземпляре StreamStatusChecker
#         await message.answer(f"URL успешно изменен на: {url}")
#     else:
#         await message.answer("Ошибка сохранения URL.")
#     await state.clear()
#
#
# async def show_url_handler(message: types.Message, user_id, get_m3u8_url):
#     url = get_m3u8_url(user_id)
#     if url:
#         await message.answer(f"Текущий URL: {url}")
#     else:
#         await message.answer("URL не установлен.")
#
# async def delete_url_handler(message: types.Message, user_id, save_m3u8_url, stream_checker):
#     if save_m3u8_url(user_id, None):  # Сохраняем None вместо URL
#         global m3u8_url  # Объявляем m3u8_url как глобальную переменную
#         m3u8_url = "http://cdn-br2.live-tv.cloud:8081/tgtv/1080i/playlist.m3u8"  # Возвращаем URL по умолчанию
#         stream_checker.m3u8_url = m3u8_url  # Изменяем url в экземпляре StreamStatusChecker
#         await message.answer("URL успешно удален и установлен на значение по умолчанию.")
#     else:
#         await message.answer("Ошибка удаления URL.")

async def show_log_handler(message: types.Message):
    # Здесь нужно реализовать логику для отображения логов.
    # Возможно, стоит читать логи из файла или базы данных.
    await message.answer("Логи пока не реализованы.")