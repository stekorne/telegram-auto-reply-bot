from loguru import logger

logger.add('logs/bot.log', rotation='10 MB', retention='3 days', encoding='utf-8', enqueue=True)
