import json
from unittest.mock import patch


def test_get_all_books(client):
    with patch("src.application.books_services.BooksService.get_all",
               return_value=[{"book_id": 1, "title": "Test Book",
                              "author": "Author"}]):
        response = client.get("/books")
        assert response.status_code == 200
        assert response.json == [{"book_id": 1,
                                  "title": "Test Book", "author": "Author"}]


def test_get_book_by_id(client):
    with patch("src.application.books_services.BooksService.get_by_id",
               return_value={"book_id": 1,
                             "title": "Test Book", "author": "Author"}):
        response = client.get("/books/1")
        assert response.status_code == 200
        assert response.json["title"] == "Test Book"


def test_get_book_by_id_not_found(client):
    with patch("src.application.books_services.BooksService.get_by_id",
               return_value=None):
        response = client.get("/books/999")
        assert response.status_code == 404


def test_add_book(client):
    book_data = {"title": "New Book", "author": "New Author"}
    with patch("src.application.books_services.BooksService.add",
               return_value={"book_id": 2, **book_data}):
        response = client.post("/books", data=json.dumps(book_data),
                               content_type="application/json")
        assert response.status_code == 201
        assert response.json["title"] == "New Book"


def test_update_book(client):
    updated_data = {"title": "Updated Title",
                    "author": "Updated Author"}
    with patch("src.application.books_services.BooksService.update",
               return_value=True):
        response = client.put("/books/1", data=json.dumps(updated_data),
                              content_type="application/json")
        assert response.status_code == 200
        assert response.json["message"] == "Book updated successfully"


def test_update_book_not_found(client):
    with patch("src.application.books_services.BooksService.update",
               return_value=False):
        response = client.put("/books/999", data=json.dumps({"title": "New"}),
                              content_type="application/json")
        assert response.status_code == 404


def test_delete_book(client):
    with patch("src.application.books_services.BooksService.delete",
               return_value=True):
        response = client.delete("/books/1")
        assert response.status_code == 200
        assert response.json["message"] == "Book deleted successfully"


def test_delete_book_not_found(client):
    with patch("src.application.books_services.BooksService.delete",
               return_value=False):
        response = client.delete("/books/999")
        assert response.status_code == 404
