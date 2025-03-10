from fastapi import HTTPException
from starlette import status


class AppException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class NotFoundException(AppException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class AlreadyExistsException(AppException):
    def __init__(
        self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST
    ):
        super().__init__(status_code=status_code, detail=detail)


class UnauthorizedException(AppException):
    def __init__(
        self, detail: str, status_code: int = status.HTTP_401_UNAUTHORIZED
    ):
        super().__init__(status_code=status_code, detail=detail)
