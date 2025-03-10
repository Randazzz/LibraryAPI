"""initial migrations

Revision ID: f65ea21ee1a9
Revises:
Create Date: 2025-02-17 13:12:21.429369

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f65ea21ee1a9"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=32), nullable=False),
        sa.Column("biography", sa.String(length=1024), nullable=True),
        sa.Column("birth_date", sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=64), nullable=False),
        sa.Column("description", sa.String(length=256), nullable=True),
        sa.Column("published_at", sa.Date(), nullable=False),
        sa.Column("available_copies", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "genres",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=16), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("email", sa.String(length=64), nullable=False),
        sa.Column("first_name", sa.String(length=16), nullable=False),
        sa.Column("last_name", sa.String(length=16), nullable=False),
        sa.Column("hashed_password", sa.LargeBinary(), nullable=False),
        sa.Column(
            "role", sa.Enum("ADMIN", "READER", name="role"), nullable=False
        ),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("id"),
    )
    op.create_table(
        "book_author_association",
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["author_id"], ["authors.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("book_id", "author_id"),
    )
    op.create_table(
        "book_genre_association",
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("genre_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["genre_id"], ["genres.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("book_id", "genre_id"),
    )
    op.create_table(
        "book_loans",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("loan_date", sa.DateTime(), nullable=False),
        sa.Column("return_date", sa.DateTime(), nullable=False),
        sa.Column("returned", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["book_id"],
            ["books.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("book_loans")
    op.drop_table("book_genre_association")
    op.drop_table("book_author_association")
    op.drop_table("users")
    op.drop_table("genres")
    op.drop_table("books")
    op.drop_table("authors")
    # ### end Alembic commands ###
