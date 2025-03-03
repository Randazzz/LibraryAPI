from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
    def __init__(self, detail="User not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class InvalidTokenException(HTTPException):
    def __init__(self, detail="Invalid token"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )


# fmt: off
class PermissionDeniedException(HTTPException):
    def __init__(self, detail="Permission denied"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )
# fmt: on
