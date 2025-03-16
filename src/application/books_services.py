from typing import Optional
import uuid
from src.domain.books_entity import BookEntity
from src.infrastructure.unit_of_work.unit_of_work import UnitOfWork


class BooksService:
    def get_all(self):
        with UnitOfWork() as uow:
            assert uow.books_repo is not None
            return uow.books_repo.get_all()

    def get_by_id(self, book_id: int):
        with UnitOfWork() as uow:
            assert uow.books_repo is not None
            return uow.books_repo.get_by_id(book_id)

    def add(self, book_data: dict):
        with UnitOfWork() as uow:
            assert uow.books_repo is not None
            result = uow.books_repo.add(book_data)
            uow.commit()
            return result

    def update(self, book_id: int, book_data: dict):
        with UnitOfWork() as uow:
            assert uow.books_repo is not None
            result = uow.books_repo.update(book_id, book_data)
            if result:
                uow.commit()
            return result

    def delete(self, book_id: int):
        with UnitOfWork() as uow:
            assert uow.books_repo is not None
            result = uow.books_repo.delete(book_id)
            if result:
                uow.commit()
            return result

    def borrow_book(self, book_id: int, members_id: str) -> Optional[dict]:
        with UnitOfWork() as uow:
            assert uow.books_repo is not None
            assert uow.members_repo is not None
        try:
            book = uow.books_repo.get_by_id_for_update(book_id)
            if not book:
                return {"error": "Book not found"}

            if book["is_borrowed"]:
                return {"error": "Book is already borrowed"}

            member = uow.members_repo.get_by_id(str(members_id))
            if not member:
                return {"error": "Member not found"}

            book_entity = BookEntity(**book)
            book_entity.borrow(uuid.UUID(members_id))

            updated = uow.books_repo.update(book_id, {
                "is_borrowed": True,
                "borrowed_date": book_entity.borrowed_date,
                "borrowed_by": uuid.UUID(members_id)
            })

            if updated:
                print("✅ Committing transaction...")
                uow.commit()
                return {"message": "Book borrowed successfully"}
            return {"error": "Failed to borrow book"}

        except Exception as e:
                print(f"❌ REAL DATABASE ERROR: {e}")
                return {"error": f"Database error: {str(e)}"}

    def return_book(self, book_id: int) -> Optional[dict]:
        with UnitOfWork() as uow:
            assert uow.books_repo is not None

            book = uow.books_repo.get_by_id(book_id)
            if not book:
                return {"error": "Book not found"}

            if not book["is_borrowed"]:
                return {"error": "Book is not currently borrowed"}

            book_entity = BookEntity(**book)
            book_entity.return_book()

            updated = uow.books_repo.update(book_id, {
                "is_borrowed": False,
                "borrowed_date": None,
                "borrowed_by": None
            })

            if updated:
                uow.commit()
                return {"message": "Book returned successfully"}
            return {"error": "Failed to return book"}
