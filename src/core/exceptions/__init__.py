from .already_exists import (
    AuthorAlreadyExistsException,
    BookAlreadyExistsException,
    GenreAlreadyExistsException,
    UserAlreadyExistsException,
)
from .database import DatabaseConnectionException
from .not_found import (
    AuthorNotFoundException,
    GenreNotFoundException,
    UserNotFoundException,
)
from .unauthorized import (
    InvalidCredentialException,
    InvalidTokenException,
    InvalidTokenTypeException,
    PermissionDeniedException,
)
