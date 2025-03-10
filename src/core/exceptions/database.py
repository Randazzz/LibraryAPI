from starlette import status

from src.core.exceptions.base import AppException
from src.core.exceptions.messages import ErrorMessage


class DatabaseConnectionException(AppException):
    def __init__(self, detail: str = ErrorMessage.DATABASE_CONNECTION_ERROR):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail
        )
