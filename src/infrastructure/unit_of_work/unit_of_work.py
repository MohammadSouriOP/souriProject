from types import TracebackType
from typing import Optional, Type

from sqlalchemy.orm import Session

from src.infrastructure.database.connection import get_session
from src.infrastructure.repo.book_repo import BooksRepo
from src.infrastructure.repo.member_repo import MembersRepo


class UnitOfWork:
    def __init__(self) -> None:
        self.session: Optional[Session] = None
        self.books_repo: Optional[BooksRepo] = None
        self.members_repo: Optional[MembersRepo] = None

    def __enter__(self) -> "UnitOfWork":
        self.session = get_session()
        self.books_repo = BooksRepo(self.session)
        self.members_repo = MembersRepo(self.session)
        return self

    def commit(self) -> None:
        if self.session:
            try:
                self.session.commit()
            except Exception as e:
                self.rollback()
                raise e

    def rollback(self) -> None:
        if self.session:
            self.session.rollback()

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_value: Optional[BaseException],
            traceback: Optional[TracebackType]
            ) -> None:
        if exc_type:
            self.rollback()
        if self.session:
            self.session.close()
