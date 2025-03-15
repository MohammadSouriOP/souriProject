from types import TracebackType
from typing import Optional, Type

from sqlalchemy.orm import Session

from src.infrastrucutre.database.connection import get_session
from src.infrastrucutre.repo.book_repo import BooksRepo  # Import BooksRepo


class UnitOfWork:
    def __init__(self) -> None:
        self.session: Optional[Session] = None
        self.repo: Optional[BooksRepo] = None

    def __enter__(self) -> "UnitOfWork":
        self.session = get_session()
        self.repo = BooksRepo(self.session)
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

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        if exc_type:
            self.rollback()
        if self.session:
            self.session.close()
