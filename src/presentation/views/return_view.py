from flask import Response, abort, jsonify
from flask.views import MethodView

from src.application.books_services import BooksService


class ReturnView(MethodView):
    def __init__(self) -> None:
        self.service = BooksService()

    def post(self, book_id: int) -> Response:
        result = self.service.return_book(book_id) or {}
        if "error" in result:
            abort(400, description=result["error"])
        return jsonify(result)
