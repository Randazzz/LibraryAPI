import uuid
from typing import Annotated

from pydantic import EmailStr
from sqlalchemy import UUID, String
from sqlalchemy.orm import DeclarativeBase, mapped_column

intpk = Annotated[int, mapped_column(primary_key=True)]
uuidpk = Annotated[
    uuid.UUID,
    mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    ),
]
str_16 = Annotated[str, "str_16"]
str_32 = Annotated[str, "str_32"]
str_64 = Annotated[str, "str_64"]
str_128 = Annotated[str, "str_128"]
str_256 = Annotated[str, "str_256"]
str_1024 = Annotated[str, "str_1024"]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_16: String(16),
        str_32: String(32),
        str_64: String(64),
        str_128: String(128),
        str_256: String(256),
        str_1024: String(1024),
        EmailStr: String(64),
    }
