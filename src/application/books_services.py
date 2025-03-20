import uuid

from src.domain.books_entity import BookEntity
from src.infrastructure.unit_of_work.unit_of_work import UnitOfWork


class BooksService:
    def get_all(self):
        with UnitOfWork() as uow:
            assert uow.books_repo is not None
            return uow.books_repo.get_all(uow.connection)

    def get_by_id(self, book_id: int):
        with UnitOfWork() as uow:
            assert uow.books_repo is not None
            return uow.books_repo.get(str(book_id), uow.connection)

    def add(self, book_data: BookEntity):
        with UnitOfWork() as uow:
            assert uow.books_repo is not None
            result = uow.books_repo.create(book_data, uow.connection)
            uow.commit()
            return result

    def update(self, book_id: int, book_data: dict):
        with UnitOfWork() as uow:
            assert uow.books_repo is not None
            result = uow.books_repo.update(str(book_id),
                                           book_data, uow.connection)
            if result:
                uow.commit()
            return result

    def delete(self, book_id: int):
        with UnitOfWork() as uow:
            assert uow.books_repo is not None
            result = uow.books_repo.delete(str(book_id), uow.connection)
            if result:
                uow.commit()
            return result

    def borrow_book(self, book_id: int, members_id: str) -> dict | None:
        with UnitOfWork() as uow:
            assert uow.books_repo is not None
            assert uow.members_repo is not None

            book_data = uow.books_repo.get(str(book_id), uow.connection)
            if not book_data:
                return {"error": "Book not found"}

            book = book_data

            if book.is_borrowed:
                return {"error": "Book is already borrowed"}

            member_id = str(member_id)
            member = uow.members_repo.get_by_id(member_id, uow.connection)
            if not member:
                return {"error": "Member not found"}

            book_entity = book
            book_entity.borrow(uuid.UUID(members_id))

            updated = uow.books_repo.update(str(book_id), {
                "is_borrowed": True,
                "borrowed_date": book_entity.borrowed_date,
                "borrowed_by": uuid.UUID(members_id)
            }, uow.connection)

            if updated:
                uow.commit()
                return {"message": "Book borrowed successfully"}
            return {"error": "Failed to borrow book"}

    def return_book(self, book_id: int) -> dict | None:
        with UnitOfWork() as uow:
            assert uow.books_repo is not None

            book_data = uow.books_repo.get(str(book_id), uow.connection)
            if not book_data:
                return {"error": "Book not found"}

            if not isinstance(book_data, dict):
                return {"error": "Invalid book data"}

            book_entity = BookEntity(**book_data)
            if not book_entity.is_borrowed:
                return {"error": "Book is not currently borrowed"}
            book_entity.return_book()

            updated = uow.books_repo.update(book_id, {
                "is_borrowed": False,
                "borrowed_date": None,
                "borrowed_by": None
            }, uow.connection)

            if updated:
                uow.commit()
                return {"message": "Book returned successfully"}
            return {"error": "Failed to return book"}
