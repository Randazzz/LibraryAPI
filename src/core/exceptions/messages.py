from enum import Enum


class ErrorMessage(str, Enum):
    USER_ALREADY_EXISTS = "User with this email already exists"
    AUTHOR_ALREADY_EXISTS = "Author with this name already exists"
    BOOK_ALREADY_EXISTS = "Book with this title already exists"
    GENRE_ALREADY_EXISTS = "Genre with this name already exists"
    BOOK_LOAN_ALREADY_EXISTS = "This book has already been issued to the user"

    USER_NOT_FOUND = "User not found"
    AUTHOR_NOT_FOUND = "Author not found"
    GENRE_NOT_FOUND = "Genre not found"
    BOOK_NOT_FOUND = "Book not found"
    BOOK_COPY_NOT_FOUND = "No copies available"
    BOOK_LOAN_NOT_FOUND = "Book loan not found"

    INVALID_TOKEN = "Invalid token"
    PERMISSION_DENIED = "Permission denied"
    INVALID_CREDENTIALS = "Invalid credentials"
    INVALID_TOKEN_TYPE = "Invalid token type '{current_token_type}' expected '{expected_token_type}'"

    DATABASE_CONNECTION_ERROR = "Database connection error"

    BOOK_LIMIT_EXCEEDED = "Book limit exceeded for one user"
