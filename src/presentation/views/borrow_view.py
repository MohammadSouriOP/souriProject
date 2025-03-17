from flask import Response, jsonify
from flask.views import MethodView

from src.application.books_services import BooksService
from src.presentation.errors_handlers.borrow_errors import BorrowErrors


class BorrowView(MethodView):
    def __init__(self) -> None:
        self.service = BooksService()

    def post(self, book_id: int, members_id: str) -> Response:
        try:
            result = self.service.borrow_book(book_id, members_id)
            if result is None:
                return BorrowErrors.book_not_found()
            return jsonify(result)

        except ValueError:
            return BorrowErrors.already_borrowed()

        except KeyError:
            return BorrowErrors.book_not_found()

        except Exception as e:
            print(f"Unexpected error: {e}")
            return BorrowErrors.database_error()
