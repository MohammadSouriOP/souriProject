from types import TracebackType
from typing import Type

from sqlalchemy.engine import Connection, RootTransaction

from src.infrastructure.database.connection import get_connection
from src.infrastructure.repo.book_repo import BooksRepo
from src.infrastructure.repo.member_repo import MembersRepo


class UnitOfWork:
    def __init__(self) -> None:
        self.connection: Connection = get_connection()
        self.books_repo: BooksRepo = BooksRepo(self.connection)
        self.members_repo: MembersRepo = MembersRepo(self.connection)
        self.transaction: RootTransaction | None = None  # Ensure it's properly initialized

    def __enter__(self) -> "UnitOfWork":
        self.transaction = self.connection.begin()  # Always begin a new transaction
        return self

    def commit(self) -> None:
        if not self.transaction or not self.transaction.is_active:
            raise RuntimeError("Cannot commit: Transaction is inactive.")
        try:
            self.transaction.commit()
        except Exception as e:
            print("Error during commit, rolling back...")
            self.rollback()
            raise e

    def rollback(self) -> None:
        if self.transaction and self.transaction.is_active:
            print('Rolling back transaction...')
            self.transaction.rollback()

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None
    ) -> None:
        if exc_type:
            print("Rolling back due to exception:", exc_type)
            self.rollback()
        if self.connection:
            self.connection.close()
