from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.db.models.books import BookLoan
else:
    BookLoan = "BookLoan"

from pydantic import EmailStr
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base, str_16, uuidpk


class Role(str, Enum):
    ADMIN = "admin"
    READER = "reader"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuidpk]
    email: Mapped[EmailStr] = mapped_column(unique=True, nullable=False)
    first_name: Mapped[str_16] = mapped_column(nullable=False)
    last_name: Mapped[str_16] = mapped_column(nullable=False)
    hashed_password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    role: Mapped[Role] = mapped_column(
        SQLAlchemyEnum(Role), nullable=False, default=Role.READER
    )
    book_loans: Mapped[list["BookLoan"]] = relationship(
        "BookLoan", back_populates="user"
    )
    is_superuser: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f"<User(email='{self.email}', role='{self.role}')>"
