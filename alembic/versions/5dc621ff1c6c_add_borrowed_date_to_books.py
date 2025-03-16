"""Add borrowed_date to books

Revision ID: 5dc621ff1c6c
Revises: 8bc88e1d8061
Create Date: 2025-03-16 00:39:40.318923

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '5dc621ff1c6c'
down_revision: Union[str, None] = '8bc88e1d8061'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('borrowed_date', sa.DateTime(), nullable=True))
    op.add_column('books', sa.Column('borrowed_by', sa.UUID(), nullable=True))
    op.create_foreign_key(None, 'books', 'members', ['borrowed_by'], ['members_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'books', type_='foreignkey')
    op.drop_column('books', 'borrowed_by')
    op.drop_column('books', 'borrowed_date')
    # ### end Alembic commands ###
