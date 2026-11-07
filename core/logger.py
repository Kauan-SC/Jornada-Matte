import logging

from config import DISCORD_WEBHOOK_URL
from discord_logging.handler import DiscordHandler

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

discord_format = logging.Formatter("%(name)s | Pode%(levelname)s | %(message)s")


#  Notificação de Errors
if DISCORD_WEBHOOK_URL is not None:

    discord_handler = DiscordHandler(
        "Serverless Errors - Jornada Matte",
        DISCORD_WEBHOOK_URL,)

    discord_handler.setLevel(logging.ERROR)
    discord_handler.setFormatter(discord_format)
    logger.addHandler(discord_handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)