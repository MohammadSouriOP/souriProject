from flask import Response, jsonify, make_response
from flask.views import MethodView

from src.application.books_services import BooksService


class ReturnView(MethodView):
    def __init__(self) -> None:
        self.service = BooksService()

    def post(self, book_id: int) -> Response:
        result = self.service.return_book(book_id) or {}
        if "error" in result:
            return make_response(jsonify(result), 400)
        return jsonify(result)
