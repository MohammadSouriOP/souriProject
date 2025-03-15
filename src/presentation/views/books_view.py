from typing import Any, Dict, Optional

from flask import Response, abort, jsonify, make_response, request
from flask.views import MethodView

from src.application.books_services import BooksService


class BooksView(MethodView):
    def __init__(self) -> None:
        self.service = BooksService()

    def get(self, book_id: Optional[int] = None) -> Response:
        if book_id is None:
            books = self.service.get_all()
            return make_response(jsonify(books or []), 200)

        book: Optional[Dict[str, Any]] = self.service.get_by_id(book_id)
        if book is None:
            abort(404, description="Book not found")

        return jsonify(book)

    def post(self) -> Response:
        data = request.get_json()
        if not data:
            abort(400, description="Invalid data")

        entity = {
            "title": data.get("title"),
            "author": data.get("author")
        }
        if not all([entity["title"], entity["author"]]):
            abort(400, description="Required fields missing")

        result = self.service.add(entity)
        if result:
            return make_response(jsonify(result), 201)
        abort(500, description="Error adding book")

    def put(self, book_id: int) -> Response:
        data = request.get_json()
        if not data:
            abort(400, description="Invalid JSON data")

        entity = {
            "title": data.get("title"),
            "author": data.get("author")
        }

        result = self.service.update(book_id, entity)
        if not result:
            abort(404, description="Book not found")
        return jsonify(message="Book updated successfully")

    def delete(self, book_id: int) -> Response:
        result = self.service.delete(book_id)
        if not result:
            abort(404, description="Book not found")

        return jsonify(message="Book deleted successfully")
