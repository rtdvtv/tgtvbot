import aiohttp
import asyncio
import logging
import requests
import re


# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class StreamStatusChecker:
    def __init__(self, m3u8_url: str, default_interval: int = 60):
        self.m3u8_url = m3u8_url
        self.current_interval = max(default_interval, 60)  # Интервал по умолчанию, но не менее 60 сек.
        self.is_stream_online = False
        self.task = None

    def stop_monitoring(self):
        """Останавливаем мониторинг потока."""
        if self.task and not self.task.done():
            self.task.cancel()
            self.task = None
            logging.info("Мониторинг потока остановлен")
        else:
            logging.info("Мониторинг потока не запущен или уже остановлен")

    # Мониторинг в фоне
    async def monitor_stream(self, chat_id: int, bot):
        """Мониторим поток в фоне."""
        while True:
            try:
                status = await self.check_stream_status()
                if status != self.is_stream_online:
                    self.is_stream_online = status
                    if status:
                        green_circle = '\U0001F7E2'
                        await bot.send_message(chat_id, f"{green_circle} Status: Run-Stream ONLINE")

                        logging.info("Log:Run-Stream-ONLINE")
                    else:
                        red_circle = '\U0001F534'
                        await bot.send_message(chat_id, f"{red_circle} Status: Stream-Error OFFLINE")
                        logging.error("Log:Stream-Error-OFFLINE")
            except Exception as e:
                logging.exception(f"ERROR в monitor_stream: {e}")
            await asyncio.sleep(self.current_interval)
            print("Monitor_Stream")

    def start_monitoring(self, chat_id: int, bot):
        """Запускаем мониторинг в фоне."""
        if self.task is None:
            try:
                self.task = asyncio.create_task(self.monitor_stream(chat_id, bot))
                logging.info("Запущен мониторинг потока")
            except Exception as e:
                logging.exception(f"Ошибка запуска мониторинга: {e}")

    async def check_stream_status(self) -> bool:
        """
        Проверяю доступность потока (m3u8). Возвращаем True, если доступен, иначе False.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.m3u8_url, timeout=10) as response:
                    return response.status == 200
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:  # Ловим конкретные исключения
            logging.error(f"Ошибка проверки статуса потока: {e}")  # Логируем ошибку
            print("check_stream_status")
            return False

def start_monitoring(self, chat_id: int, bot):
        """
        Запускаем мониторинг в фоне только один раз.
        """
        if self.task is None:  # Проверяем, не запущена ли уже задача
            self.task = asyncio.create_task(self.monitor_stream(chat_id, bot))
            print("start_monitoring")


# Блок анализа потока: Битрейт и размер изображения
def get_m3u8_info(m3u8_url: str) -> dict:
    try:
        response = requests.get(m3u8_url)
        response.raise_for_status()  # Проверка на ошибки HTTP

        m3u8_content = response.text

        # Поиск битрейта
        bandwidth_match = re.search(r'BANDWIDTH=(\d+)', m3u8_content)
        bitrate = int(bandwidth_match.group(1)) if bandwidth_match else None

        # Поиск разрешения (размера картинки)
        resolution_match = re.search(r'RESOLUTION=(\d+x\d+)', m3u8_content)
        resolution = resolution_match.group(1) if resolution_match else None

        return {
            'bitrate': bitrate,
            'resolution': resolution}

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке M3U8: {e}")
        return None
    except AttributeError:
        print("Информация о битрейте или разрешении не найдена в M3U8.")
        return None

# Пример использования
m3u8_url = 'http://cdn-br2.live-tv.cloud:8081/tgtv/1080i/playlist.m3u8'  # Замените на URL вашего M3U8-файла
info = get_m3u8_info(m3u8_url)

if info:
    print(f"Битрейт: {info['bitrate']} bps")
    print(f"Разрешение: {info['resolution']}")