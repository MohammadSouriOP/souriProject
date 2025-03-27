from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class BookModel(BaseModel):
    id: int
    title: str
    author: str
    is_borrowed: bool
    borrowed_date: Optional[datetime] = None
    borrowed_by: Optional[UUID] = None

    class Config:
        orm_mode = True
