from aiogram import Bot, Dispatcher, F, Router
from aiogram.fsm.storage.memory import MemoryStorage
# from status_str import StreamStatusChecker
# from db_mbot import initialize_database, connection
from config import BOT_TOKEN
from handlers import router, stream_checker
from handlers_key import register_echo_handlers

dp = Dispatcher()

# Создаем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
# dp = Dispatcher(storage=storage)

# Инициализация базы данных
# initialize_database()


# ### БД Завершение
# async def shutdown():
#     print("Отключение бота и закрытие соединения с базой данных...")
#     connection.close()

### Главная функция
async def main():
    dp.include_router(router)
    register_echo_handlers(dp)  #
    '''Передаем dp в функцию регистрации из echo_bot.py
    # register_handlers() # Передаем dp в функцию регистрации из mbot.py'''

    print("Бот запущен и пашет как коняка!")
    try:
        # Запускаем мониторинг сразу после запуска бота
        stream_checker.start_monitoring(chat_id=520410415, bot=bot)  # Указываем ваш chat_id
        # Удаляем вебхуки, если есть
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("Бот остановлен!")
    # finally:
    #     await shutdown()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())