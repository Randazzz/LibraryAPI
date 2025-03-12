from src.core.exceptions.base import LimitExceededException
from src.core.exceptions.messages import ErrorMessage


class BookLimitExceededException(LimitExceededException):
    def __init__(self, detail: str = ErrorMessage.BOOK_LIMIT_EXCEEDED):
        super().__init__(detail=detail)
