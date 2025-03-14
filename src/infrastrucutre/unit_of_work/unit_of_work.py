from types import TracebackType
from typing import Any, Optional, Type
from sqlalchemy.orm import Session
from src.infrastrucutre.database.connection import get_session
# from src.infra.repo.base_repo import BaseRepo


class UnitOfWork:
    def __init__(self, repo_class: BaseRepo[Any]) -> None:
        self.session: Session
        self.repo = repo_class

    def __enter__(self) -> 'UnitOfWork':
        self.session = get_session()
        self.transaction = self.session.begin()
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

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        if exc_type:
            self.rollback()
        if self.session:
            self.commit()
            self.session.close()
