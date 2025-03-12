from src.core.exceptions.base import AlreadyExistsException
from src.core.exceptions.messages import ErrorMessage


class UserAlreadyExistsException(AlreadyExistsException):
    def __init__(self, detail: str = ErrorMessage.USER_ALREADY_EXISTS):
        super().__init__(detail=detail)


class AuthorAlreadyExistsException(AlreadyExistsException):
    def __init__(self, detail: str = ErrorMessage.AUTHOR_ALREADY_EXISTS):
        super().__init__(detail=detail)


class BookAlreadyExistsException(AlreadyExistsException):
    def __init__(self, detail: str = ErrorMessage.BOOK_ALREADY_EXISTS):
        super().__init__(detail=detail)


class GenreAlreadyExistsException(AlreadyExistsException):
    def __init__(self, detail: str = ErrorMessage.GENRE_ALREADY_EXISTS):
        super().__init__(detail=detail)


class BookLoanAlreadyExistsException(AlreadyExistsException):
    def __init__(self, detail: str = ErrorMessage.BOOK_LOAN_ALREADY_EXISTS):
        super().__init__(detail=detail)
