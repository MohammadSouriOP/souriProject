from typing import Dict, List, Optional

from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session

from src.infrastructure.database.schema import books


class BooksRepo:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Dict]:
        query = select(books)
        result = self.session.execute(query)
        return [dict(row) for row in result.mappings().all()]

    def get_by_id(self, book_id: int) -> Optional[Dict]:
        query = select(books).where(books.c.book_id == book_id)
        result = self.session.execute(query).mappings().first()
        return dict(result) if result else None

    def add(self, book_data: Dict) -> Optional[Dict]:
        query = insert(books).values(
            title=book_data["title"],
            author=book_data["author"],
            is_borrowed=False
        ).returning(books)
        result = self.session.execute(query)
        inserted_book = result.mappings().first()
        self.session.commit()
        return dict(inserted_book) if inserted_book else None

    def update(self, book_id: int, book_data: Dict) -> Optional[Dict]:
        query = update(books).where(books.c.book_id == book_id).values(
            title=book_data.get("title"),
            author=book_data.get("author")
        ).returning(books)
        result = self.session.execute(query)
        updated_book = result.mappings().first()
        self.session.commit()
        return dict(updated_book) if updated_book else None

    def delete(self, book_id: int) -> bool:
        query = delete(books).where(books.c.book_id == book_id)
        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount > 0
