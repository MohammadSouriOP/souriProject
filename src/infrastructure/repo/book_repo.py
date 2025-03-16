from typing import Dict, List, Optional
import uuid
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

    def get_by_id_for_update(self, book_id: int) -> Optional[Dict]:
        query = select(books).where(books.c.book_id == book_id).with_for_update()
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
        current_book = self.get_by_id(book_id)
        if not current_book:
            return None 

        query = update(books).where(books.c.book_id == book_id).values(
            title=book_data.get("title", current_book["title"]),
            author=book_data.get("author", current_book["author"]),
            is_borrowed=book_data.get("is_borrowed", current_book["is_borrowed"]),
            borrowed_date=book_data.get("borrowed_date", current_book["borrowed_date"]),
            borrowed_by=str(book_data.get("borrowed_by"))
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
