from typing import Dict

from sqlalchemy import select
from sqlalchemy.engine import Connection

from src.domain.books_entity import BookEntity
from src.infrastructure.database.schema import books, members
from src.infrastructure.repo.base_repo import BaseRepo


class BooksRepo(BaseRepo[BookEntity]):
    def __init__(self, connection: Connection) -> None:
        super().__init__(BookEntity, books)
        self.connection = connection

    def get_borrowed_book_with_member(self, book_id: str,
                                      connection: Connection) -> Dict | None:
        query = (
            select(
                books.c.book_id,
                books.c.title,
                books.c.author,
                books.c.is_borrowed,
                books.c.borrowed_date,
                members.c.member_id,
                members.c.name.label("member_name"),
                members.c.email.label("member_email"),
            )
            .join(members, books.c.borrowed_by == members.c.member_id)
            .where(books.c.book_id == book_id)
        )

        result = connection.execute(query).first()
        return dict(result._mapping) if result else None
