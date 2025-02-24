from aiogram import F, types
from handlers import router
from aiogram.fsm.context import FSMContext

# обработчики для инлайн-кнопок RU и EN
@router.callback_query(F.data == "ru_info")
async def ru_info(callback: types.CallbackQuery, state: FSMContext):
    description = """
Telegram-бот "RTDVTV Monitor" — это профессиональное решение для мониторинга потоков в формате M3U8.
Бот разработан для пользователей, которым необходимо отслеживать статус потоков, 
получать уведомления об изменениях статуса потока. Создавать и управлять списком ссылок для мониторинга.

Основные функции бота:
Мониторинг потоков:
    - Бот постоянно проверяет статус потока после запуска команды RUN или нажатия кнопки CHECK.
    - В фоновом режиме бот отслеживает доступность потока и уведомляет пользователя о его статусе (**ONLINE**/**OFFLINE**).
    - Пользователь может просматривать параметры потока, такие как битрейт и размер изображения.

Управление списком потоков:
    - Бот позволяет добавлять, удалять и просматривать ссылки на потоки.
    - Пользователь может выбрать конкретную ссылку для мониторинга или просмотра в режиме реального времени.
    - Поддерживается возможность редактирования списка ссылок через интерактивное меню.

Встроенный текстовый ИИ (Ai-Mistral):
    - Бот оснащен текстовым ИИ с функцией контекста, который можно активировать или деактивировать по команде.
    - Бот позволяет работать с ИИ не прерывая процесс мониторинга.

Планировщик событий (SCHEDULER):
    - Бот поддерживает создание напоминаний и автоматическое добавление ссылок для мониторинга в установленное время автоматическом режиме.
    - Пользователь может настроить уведомления о событиях, которые будут отправляться в указанное время.

Уведомления и рассылка:
    - Бот отправляет уведомления об изменениях статуса потока.
    - Пользователь может настроить отправку уведомлений отдельным пользователям.

Интерактивное меню:
    - Бот оснащен удобным меню с кнопками для быстрого доступа к основным функциям.
    - Пользователь может легко переключаться между разделами: мониторинг, настройки, ИИ, планировщик и т.д.
    - Меню адаптировано для использования как на мобильных устройствах, так и на компьютерах.

Автоматизация мониторинга: 
    - **Автоматизация:** Бот работает в фоновом и ручном режимах. 
    - Гибкость:** Возможность добавлять и управлять списком потоков, а также настраивать уведомления.
    - Интеграция ИИ:** Встроенный текстовый ИИ расширяет функционал бота, делая его универсальным инструментом.
    - Простота использования:** Интуитивно понятное меню и команды делают бота доступным для пользователей любого уровня подготовки.

Пример использования:
    1. Пользователь запускает бота командой **/start**.
    2. Добавляет ссылку на поток через меню **URL_STR**.
    3. Запускает мониторинг командой **RUN**.
    4. Получает уведомления о статусе потока (ONLINE/OFFLINE).
    5. При запросе "STR_INFO" получает параметры потока.
    6. Использует текстовый ИИ для получения дополнительной информации.
    7. Настраивает планировщик для автоматического мониторинга в определенное время.

<b>Технические особенности</b>:
    - Язык программирования и библиотеки:Python/ Aiogram/ SQLite
    - Библиотеки:** Aiogram, Sqlalchemy, m3u8, Asyncio, FsmStorage.
    - База данных:** SQLite.
    - Интеграция: Поддержка Telegram API, текстовый ИИ на базе Mistral

    **Created by "RTDVTV"** (rtdvtv@gmail.com)
    """

    message = await callback.message.answer(description)
    await state.update_data(description_message_id=message.message_id)
    await callback.answer()

    # await callback.message.answer(description)
    # await callback.answer()  # Убираем индикатор загрузки
    await callback.message.edit_reply_markup(reply_markup=None)  # Удаляем инлайн клавиатуру


@router.callback_query(F.data == "en_info")
async def en_info(callback: types.CallbackQuery, state: FSMContext):
    description = """
The Telegram bot "RTDVTV Monitor" is a professional solution for monitoring M3U8 streams. 
Designed for users who need to track stream statuses, receive notifications about changes, a
nd manage a list of links for monitoring, the bot also features a built-in text AI and an event scheduler, 
making it a versatile tool for working with media streams.

Key Features of the Bot

Stream Monitoring:
    - The bot continuously checks the stream status after the **RUN** command is executed or the **CHECK** button is pressed.
    - In the background, the bot monitors stream availability and notifies the user of its status (ONLINE/OFFLINE).
    - Users can view stream parameters such as bitrate and image size.

Stream List Management:
    - The bot allows users to add, delete, and view stream links.
    - Users can select a specific link for monitoring or real-time viewing.
    - The bot supports editing the list of links through an interactive menu.

Built-in Text AI:
   - The bot is equipped with a text AI that can be activated or deactivated on command.
   - The AI enables users to ask questions and receive answers without interrupting the stream monitoring process.

Event Scheduler:
    - The bot supports creating reminders and automatically adding links for monitoring at specified times.
    - Users can configure event notifications to be sent at designated times.
    - The scheduler allows for flexible task management and automation of routine processes.

Notifications and Broadcasting:
    - The bot sends notifications about stream status changes.
    - Users can configure notifications to be sent to specific users or groups.
    - Notifications can be personalized based on user preferences.

Interactive Menu:
    - The bot features a user-friendly menu with buttons for quick access to core functions.
    - Users can easily switch between sections: monitoring, settings, AI, scheduler, etc.
    - The menu is optimized for use on both mobile devices and computers.

Advantages of the Bot:
    - Automation of Monitoring:** The bot operates in the background, allowing users to focus on other tasks.
    - Flexibility:** Users can add and manage a list of streams and customize notifications.
    - AI Integration:** The built-in text AI enhances the bot's functionality, making it a versatile tool.
    - Ease of Use:** An intuitive menu and commands make the bot accessible to users of all skill levels.
    - Reliability:** The bot utilizes modern technologies to ensure stable operation and accuracy for software or visual monitoring.

Example of Use
1. The user starts the bot with the **/start** command.
2. Adds a stream link via the **URL_STR** menu.
3. Initiates monitoring with the **RUN** command.
4. Receives notifications about the stream status (ONLINE/OFFLINE).
5. Requests "STR_INFO" to obtain stream parameters.
6. Uses the text AI to get additional information.
7. Configures the scheduler for automatic monitoring at specified times.

Technical Specifications:
- **Programming Language:** Python
- **Libraries:** aiogram, sqlalchemy, m3u8, asyncio
- **Database:** SQLite for storing user data, stream lists, and user settings.
- **Integration:** Telegram API support, text AI based on Mistral.

Created by "RTDVTV" (rtdvtv@gmail.com)
    """

    message = await callback.message.answer(description)
    await state.update_data(description_message_id=message.message_id)
    await callback.answer()

    # await callback.message.answer(description)
    # await callback.answer()  # Убираем индикатор загрузки
    await callback.message.edit_reply_markup(reply_markup=None)  # Удаляем инлайн клавиатуру