import logging
import requests
import hmac
import hashlib
import time
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
from config import TRADE_CONFIG  # Импортируем конфигурацию

# Загружаем переменные окружения из .env файла
load_dotenv()

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация для BingX
API_KEY = os.getenv('BINGX_API_KEY')
SECRET_KEY = os.getenv('BINGX_SECRET_KEY')
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


# Функция для создания подписи для запроса к BingX
def generate_signature(payload):
    query_string = '&'.join([f"{key}={payload[key]}" for key in sorted(payload.keys())])
    return hmac.new(SECRET_KEY.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()


# Функция для открытия позиции на BingX
def open_position(symbol, side):
    url = 'https://api.bingx.com/v1/order/place'
    timestamp = int(time.time() * 1000)

    # Получаем настройки из конфигурации
    config = TRADE_CONFIG.get(symbol, TRADE_CONFIG['default'])
    position_size = config['position_size']
    leverage = config['leverage']

    payload = {
        'symbol': symbol,
        'side': side,
        'type': 'market',
        'quantity': position_size,
        'leverage': leverage,
        'timestamp': timestamp,
        'api_key': API_KEY
    }

    # Здесь вы можете рассчитывать стоп-лосс и тейк-профит
    # Например, если у вас есть текущая цена, вы можете добавить их в payload

    response = requests.post(url, json=payload)
    return response.json()


# Функция обработки текстовых сообщений
def handle_message(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    logger.info(f"Received message: {message_text}")

    if "buy" in message_text:
        response = open_position('BTCUSDT', 'buy')  # Замените 'BTCUSDT' на нужный вам символ
        update.message.reply_text(f"Ответ от BingX: {response}")
    elif "sell" in message_text:
        response = open_position('BTCUSDT', 'sell')  # Замените 'BTCUSDT' на нужный вам символ
        update.message.reply_text(f"Ответ от BingX: {response}")
    else:
        update.message.reply_text("Неизвестная команда.")


def main():
    updater = Updater(TOKEN)

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Обработчик текстовых сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запускаем бота
    updater.start_polling()

    # Бот будет работать до тех пор, пока вы не нажмете Ctrl+C
    updater.idle()


if __name__ == '__main