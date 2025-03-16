import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '3e6a2f591c57'
down_revision = '5dc621ff1c6c'
branch_labels = None
depends_on = None

def upgrade():
    """Upgrade schema: rename book_id to id and fix foreign keys if necessary."""
    
    # Drop the foreign key constraint if it exists
    op.drop_constraint('fk_books_book_id', 'books', type_='foreignkey')

    # Rename the column
    op.alter_column('books', 'book_id', new_column_name='id')

    # Recreate the foreign key constraint (if needed)
    op.create_foreign_key('fk_books_id', 'books', 'other_table', ['id'], ['id'])  # Adjust table & column names

def downgrade():
    """Downgrade schema: revert id back to book_id."""
    
    # Drop the new foreign key constraint
    op.drop_constraint('fk_books_id', 'books', type_='foreignkey')

    # Rename column back
    op.alter_column('books', 'id', new_column_name='book_id')

    # Recreate the original foreign key
    op.create_foreign_key('fk_books_book_id', 'books', 'other_table', ['book_id'], ['id'])  # Adjust table & column names
