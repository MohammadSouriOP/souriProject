import uuid
from unittest.mock import patch


def test_borrow_book(client):
    book_id = 1
    member_id = str(uuid.uuid4())
    with patch('src.application.books_services.BooksService.borrow_book',
               return_value={
                   'id': book_id, 'title': 'Borrowed Book', 'author': 'Author',
                   'is_borrowed': True,
                   'borrowed_date': '2025-03-27T12:00:00',
                   'borrowed_by': member_id
               }):
        response = client.post(f'/borrow/{book_id}/{member_id}')
        assert response.status_code == 200
        assert response.json()['borrowed_by'] == member_id


def test_borrow_book_already_borrowed(client):
    with patch('src.application.books_services.BooksService.borrow_book',
               side_effect=ValueError):
        response = client.post(f'/borrow/1/{uuid.uuid4()}')
        assert response.status_code == 400


def test_borrow_book_not_found(client):
    with patch('src.application.books_services.BooksService.borrow_book',
               return_value=None):
        response = client.post(f'/borrow/999/{uuid.uuid4()}')
        assert response.status_code == 404
