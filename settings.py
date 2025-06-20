import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = int(os.getenv('DEBUG')) == 1

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не найден в окружении")
