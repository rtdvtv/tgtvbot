from mistralai import Mistral
from config import MISTRAL_API_KEY, BOT_TOKEN  # Импортируем токен бота

async def main_mistral(content):
    try:
        mistral = Mistral(api_key=MISTRAL_API_KEY)
        res = await mistral.chat.complete_async(
            model="mistral-small-latest",
            messages=[
                {"content": content, "role": "user"}],
            stream=False)
        return res.choices[0].message.content
    except Exception as e:  # Обработка ошибок
        print(f"Ошибка при запросе к Mistral API: {e}")
        return "Ошибка при обработке запроса."  # Или другое сообщение об ошибке
