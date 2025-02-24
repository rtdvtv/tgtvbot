


async def help_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
Этот бот предназначен для мониторинга m3u8 плейлиста. \n

Описание функций и информационных сообщений:
StrStatus-ONLINE - сообщение из фонового мониторинга при изменеии статуса потока
StrStatus-OFFLINE -сообщение из фонового мониторинга при изменеии статуса потока
    
    
    
    
    """
    await update.message.reply_text(help_text, reply_markup=markup)