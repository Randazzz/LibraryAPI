from starlette import status

from src.core.exceptions.base import AppException, UnauthorizedException
from src.core.exceptions.messages import ErrorMessage


class InvalidTokenException(UnauthorizedException):
    def __init__(self, detail: str = ErrorMessage.INVALID_TOKEN):
        super().__init__(detail=detail)


class PermissionDeniedException(AppException):
    def __init__(self, detail: str = ErrorMessage.PERMISSION_DENIED):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class InvalidCredentialException(UnauthorizedException):
    def __init__(self, detail: str = ErrorMessage.INVALID_CREDENTIALS):
        super().__init__(detail=detail)


class InvalidTokenTypeException(UnauthorizedException):
    def __init__(self, current_token_type: str, expected_token_type: str):
        # noinspection StrFormat
        detail = ErrorMessage.INVALID_TOKEN_TYPE.value.format(
            current_token_type=current_token_type,
            expected_token_type=expected_token_type,
        )
        super().__init__(detail=detail)
