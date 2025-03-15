from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from src.domain.base_entity import BaseEntity


@dataclass
class BookEntity(BaseEntity):
    title: str
    author: str
    is_borrowed: bool = field(default=False)
    borrowed_date: Optional[datetime] = field(default=None)
    borrowed_by: Optional[int] = field(default=None)  # Assuming member ID

    def borrow(self, member_id: int):
        """Marks the book as borrowed by a member."""
        if self.is_borrowed:
            raise ValueError("Book is already borrowed.")
        self.is_borrowed = True
        self.borrowed_date = datetime.utcnow()
        self.borrowed_by = member_id

    def return_book(self):
        """Marks the book as returned."""
        if not self.is_borrowed:
            raise ValueError("Book is not borrowed.")
        self.is_borrowed = False
        self.borrowed_date = None
        self.borrowed_by = None
