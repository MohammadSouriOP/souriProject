from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.application.books_services import BooksService
from src.domain.models.book_model import BookModel
from src.presentation.errors_handlers.borrow_errors import BorrowErrors

router = APIRouter()
service = BooksService()


@router.post("/{book_id}/{member_id}", response_model=BookModel)
def borrow_book(book_id: int, member_id: UUID):
    try:
        result = service.borrow_book(book_id, str(member_id))

        if result is None:
            raise HTTPException(status_code=404, detail="Book not found")

        return result.to_model()

    except ValueError:
        return BorrowErrors.already_borrowed()

    except KeyError:
        return BorrowErrors.member_not_found()

    except Exception as e:
        print("DEBUG: Unexpected error →", e)
        return BorrowErrors.database_error()
