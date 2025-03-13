from datetime import UTC, datetime, timedelta

from src.core.config import settings


def default_return_utc_datetime() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None) + timedelta(
        days=settings.BOOK_LOAN_DAYS
    )


def get_current_utc_datetime() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)
