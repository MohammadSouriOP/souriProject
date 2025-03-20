import uuid

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        MetaData, String, Table)
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()

books = Table(
    'books', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String),
    Column('author', String),
    Column('is_borrowed', Boolean, nullable=True),
    Column('borrowed_date', DateTime, nullable=True),
    Column('borrowed_by', UUID(as_uuid=True),
           ForeignKey('members.id'), nullable=True)
)

members = Table(
    'members', metadata,
    Column('id', UUID(as_uuid=True),
           primary_key=True, default=uuid.uuid4),
    Column('name', String),
    Column('email', String, unique=True)
)
