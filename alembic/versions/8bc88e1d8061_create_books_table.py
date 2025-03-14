"""create books table

Revision ID: 8bc88e1d8061
Revises: 
Create Date: 2025-03-15 16:56:52.514175

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bc88e1d8061'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('book_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('author', sa.String(), nullable=True),
    sa.Column('is_borrowed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('book_id')
    )
    op.create_table('members',
    sa.Column('members_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('members_id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('members')
    op.drop_table('books')
    # ### end Alembic commands ###
