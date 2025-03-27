from fastapi import APIRouter

from src.application.books_services import BooksService
from src.domain.models.book_model import BookModel
from src.presentation.errors_handlers.return_errors import ReturnErrors

router = APIRouter()
service = BooksService()


@router.post("/{book_id}", response_model=BookModel)
def return_book(book_id: int):
    try:
        result = service.return_book(book_id)

        if result is None:
            return ReturnErrors.failed_to_return()

        return result.to_model()

    except KeyError:
        return ReturnErrors.book_not_found()

    except ValueError:
        return ReturnErrors.book_not_borrowed()

    except Exception as e:
        print("DEBUG: Unexpected error →", e)
        return ReturnErrors.unknown_error()
