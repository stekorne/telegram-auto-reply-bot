import asyncio
import os
from datetime import datetime, time

import pytz
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ChatType
from aiogram.types import Message
from dotenv import load_dotenv

from auto_reply_storage import AutoReplyStorage
from logger import logger

load_dotenv()

logger.info('Запуск бота...')

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    logger.error('TELEGRAM_BOT_TOKEN не найден в .env')
    raise ValueError('TELEGRAM_BOT_TOKEN не найден в .env')

bot = Bot(token=TOKEN)
dp = Dispatcher()

WORK_START = time(9, 0)
WORK_END = time(18, 0)
TIMEZONE = pytz.timezone('Europe/Moscow')

storage = AutoReplyStorage('last_sent.json')


@dp.message(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}) & F.text)
async def handle_message(message: Message):
    logger.debug("-" * 100)
    now = datetime.now(TIMEZONE)
    weekday = now.weekday()
    current_time = now.time()
    chat_id = message.chat.id

    user = message.from_user.username or message.from_user.full_name
    logger.info(
        f'Сообщение в {now.strftime("%Y-%m-%d %H:%M:%S")} '
        f'от @{user} в "{message.chat.title}" (ID: {chat_id})'
    )

    in_work_time = (
            0 <= weekday <= 4 and
            WORK_START <= current_time <= WORK_END
    )

    if in_work_time:
        logger.info('Рабочее время — автоответ не требуется')
        return

    logger.info('Внерабочее время')

    last_time = storage.get_last_time(chat_id)
    if last_time:
        delta = (now - last_time).total_seconds()
        logger.info(f'Прошло {delta:.0f} секунд с последнего автоответа')
    else:
        logger.info('В этой группе ещё не отправлялся автоответ')

    if not last_time or (now - last_time).total_seconds() > 600:
        await message.answer(
            'Здравствуйте! Для нас очень важен ваш вопрос. '
            'Мы обязательно ответим в рабочее время (09:00–18:00, Пн–Пт)'
        )
        storage.update_time(chat_id, now)
        logger.info('Отправлен автоответ.')
    else:
        logger.info('Не отправляем — слишком рано после предыдущего')


async def main():
    logger.info('Бот запущен. Ожидает сообщения...')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
