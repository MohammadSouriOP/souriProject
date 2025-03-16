"""Rename book_id to id

Revision ID: 2247dd487c40
Revises: 3e6a2f591c57
Create Date: 2025-03-16 01:12:25.749666

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '2247dd487c40'
down_revision: Union[str, None] = '3e6a2f591c57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('books', sa.Column('book_id', sa.Integer(),
                                     autoincrement=True, nullable=True))

    op.execute("UPDATE books SET book_id = id")

    op.alter_column('books', 'book_id', nullable=False)

    op.drop_column('books', 'id')


def downgrade() -> None:
    op.add_column('books', sa.Column('id', sa.Integer(),
                                     autoincrement=True, nullable=True))

    op.execute("UPDATE books SET id = book_id")

    op.alter_column('books', 'id', nullable=False)

    op.drop_column('books', 'book_id')
