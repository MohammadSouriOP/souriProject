from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.domain.base_entity import BaseEntity


@dataclass
class BookEntity(BaseEntity):
    book_id: Optional[int] = field(default=None)
    title: str = ''
    author: str = ''
    is_borrowed: bool = field(default=False)
    borrowed_date: Optional[datetime] = field(default=None)
    borrowed_by: Optional[UUID] = field(default=None)

    def borrow(self, member_id: UUID):
        if self.is_borrowed:
            raise ValueError('This book is already borrowed by another member.')
        self.is_borrowed = True
        self.borrowed_date = datetime.utcnow()
        self.borrowed_by = member_id

    def return_book(self):
        if not self.is_borrowed:
            raise ValueError('Book is not borrowed.')
        self.is_borrowed = False
        self.borrowed_date = None
        self.borrowed_by = None
