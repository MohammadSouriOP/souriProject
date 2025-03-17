from types import TracebackType
from typing import Type
from sqlalchemy.engine import Connection
from src.infrastructure.database.connection import engine
from src.infrastructure.repo.book_repo import BooksRepo
from src.infrastructure.repo.member_repo import MembersRepo


class UnitOfWork:
    def __init__(self) -> None:
        self.connection: Connection | None = None
        self.books_repo: BooksRepo | None = None
        self.members_repo: MembersRepo | None = None
        self.transaction = None

    def __enter__(self) -> "UnitOfWork":
        self.connection = engine().connect()
        self.transaction = self.connection.begin()
        self.books_repo = BooksRepo(self.connection)
        self.members_repo = MembersRepo(self.connection)
        return self

    def commit(self) -> None:
        if self.transaction:
            try:
                self.transaction.commit()
            except Exception as e:
                self.rollback()
                raise e

    def rollback(self) -> None:
        if self.transaction:
            self.transaction.rollback()

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None
    ) -> None:
        if exc_type:
            self.rollback()
        if self.connection:
            self.connection.close()
