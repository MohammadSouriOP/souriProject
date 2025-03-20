from typing import Any, Dict

from flask import Response, abort, jsonify, make_response, request
from flask.views import MethodView

from src.application.books_services import BooksService
from src.domain.books_entity import BookEntity


class BooksView(MethodView):
    def __init__(self) -> None:
        self.service = BooksService()

    def get(self, book_id: str | None = None) -> Response:
        if book_id is None:
            books = self.service.get_all()
            return make_response(jsonify(books or []), 200)

        book: Dict[str, Any] | None = self.service.get_by_id(book_id)
        if book is None:
            abort(404, description="Book not found")

        return jsonify(book)

    def post(self) -> Response:
        data = request.get_json()
        if not data:
            abort(400, description="Invalid data")

        if not all([data.get("title"), data.get("author")]):
            abort(400, description="Required fields missing")
        ent = BookEntity(title=data["title"], author=data["author"])
        result = self.service.add(ent)
        if result:
            return make_response(jsonify(result), 201)
        abort(500, description="Error adding book")

    def put(self, book_id: str) -> Response:
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

    def patch(self, book_id: str) -> Response:
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

    def delete(self, book_id: str) -> Response:
        result = self.service.delete(book_id)
        if not result:
            abort(404, description="Book not found")

        return jsonify(message="Book deleted successfully")
