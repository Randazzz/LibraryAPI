import logging

from src.core.config import settings


def setup_logging():
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    logging.basicConfig(
        filename="logging.log",
        format="%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]",
        datefmt="%d/%m/%Y %I:%M:%S",
        filemode="a",
        encoding="utf-8",
        level=log_level,
    )
