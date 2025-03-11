from src.core.exceptions.base import NotFoundException
from src.core.exceptions.messages import ErrorMessage


class UserNotFoundException(NotFoundException):
    def __init__(self, detail: str = ErrorMessage.USER_NOT_FOUND):
        super().__init__(detail=detail)


class AuthorNotFoundException(NotFoundException):
    def __init__(self, detail: str = ErrorMessage.AUTHOR_NOT_FOUND):
        super().__init__(detail=detail)


class GenreNotFoundException(NotFoundException):
    def __init__(self, detail: str = ErrorMessage.GENRE_NOT_FOUND):
        super().__init__(detail=detail)


class BookNotFoundException(NotFoundException):
    def __init__(self, detail: str = ErrorMessage.BOOK_NOT_FOUND):
        super().__init__(detail=detail)
