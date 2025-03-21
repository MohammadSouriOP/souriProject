import uuid
from unittest.mock import patch


def test_borrow_book(client):
    book_id = 1
    member_id = str(uuid.uuid4())

    with patch('src.application.books_services.BooksService.borrow_book',
               return_value={'book_id': book_id, 'borrowed_by': member_id}):
        response = client.post(f'/borrow/{book_id}/{member_id}')
        assert response.status_code == 200
        assert response.json['book_id'] == book_id
        assert response.json['borrowed_by'] == member_id


def test_borrow_already_borrowed_book(client):
    book_id = 1
    member_id = str(uuid.uuid4())

    with patch('src.application.books_services.BooksService.borrow_book',
               side_effect=ValueError('This book is already borrowed.')):
        response = client.post(f'/borrow/{book_id}/{member_id}')
        assert response.status_code == 400
        assert response.json['error'] == (
            '''This book is already borrowed by another member.'''
            )


def test_borrow_book_not_found(client):
    book_id = 999
    member_id = str(uuid.uuid4())

    with patch('src.application.books_services.BooksService.borrow_book',
               return_value=None):
        response = client.post(f'/borrow/{book_id}/{member_id}')
        assert response.status_code == 404
        assert response.json['error'] == 'Book not found'


def test_return_book(client):
    book_id = 1

    with patch('src.application.books_services.BooksService.return_book',
               return_value={'book_id': book_id, 'is_borrowed': False}):
        response = client.post(f'/return/{book_id}')
        assert response.status_code == 200
        assert response.json['is_borrowed'] is False


def test_return_book_not_borrowed(client):
    book_id = 1

    with patch('src.application.books_services.BooksService.return_book',
               return_value={'error': 'Book is not borrowed.'}):
        response = client.post(f'/return/{book_id}')
        assert response.status_code == 400
        assert response.json['error'] == 'Book is not borrowed.'
