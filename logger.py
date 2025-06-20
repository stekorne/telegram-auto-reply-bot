import sys

from loguru import logger

from settings import DEBUG

if not DEBUG:
    logger.remove()
    logger.add(sys.stdout, format="{level} | {message}", level="INFO")
