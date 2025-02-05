from datetime import datetime, timedelta, timezone

from src.core.config import settings


def default_return_utc_datetime() -> datetime:
    return datetime.now(timezone.utc) + timedelta(days=settings.BOOK_LOAN_DAYS)


def get_current_utc_datetime() -> datetime:
    return datetime.now(timezone.utc)
