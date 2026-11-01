import logging

from config import DISCORD_WEBHOOK_URL, DISCORD_WEBHOOK_URL_ACOMPANHAMENTO
from discord_logging.handler import DiscordHandler

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

discord_format = logging.Formatter("%(name)s | Pode%(levelname)s | %(message)s")


# Filtro de Acompanhamento
class AcompanhamentoFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return getattr(record, "notify_acompanhamento", False) is True

#  Notificação de Errors
if DISCORD_WEBHOOK_URL is not None:

    discord_handler = DiscordHandler(
        "Serverless Errors - Jornada Matte",
        DISCORD_WEBHOOK_URL,)

    discord_handler.setLevel(logging.ERROR)
    discord_handler.setFormatter(discord_format)
    logger.addHandler(discord_handler)


# Acompanhamento de etapas específicas
if DISCORD_WEBHOOK_URL_ACOMPANHAMENTO is not None:

    discord_acompanhamento_handler = DiscordHandler(
        "Jornada Matte Infos",
        DISCORD_WEBHOOK_URL_ACOMPANHAMENTO,)

    discord_acompanhamento_handler.setLevel(logging.INFO)
    discord_acompanhamento_handler.setFormatter(discord_format)
    discord_acompanhamento_handler.addFilter(AcompanhamentoFilter())
    logger.addHandler(discord_acompanhamento_handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)