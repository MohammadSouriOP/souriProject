from unittest.mock import patch


def test_get_all_books(client):
    with patch('src.application.books_services.BooksService.get_all',
               return_value=[
                   {'id': 1, 'title': 'Test Book', 'author': 'Author',
                    'is_borrowed': False, 'borrowed_date': None,
                    'borrowed_by': None}
               ]):
        response = client.get('/books/')
        assert response.status_code == 200
        assert isinstance(response.json(), list)


def test_get_book_by_id(client):
    with patch('src.application.books_services.BooksService.get_by_id',
               return_value={
                   'id': 1, 'title': 'Test Book', 'author': 'Author',
                   'is_borrowed': False,
                   'borrowed_date': None, 'borrowed_by': None
               }):
        response = client.get('/books/1')
        assert response.status_code == 200
        assert response.json()['title'] == 'Test Book'


def test_add_book(client):
    book_data = {'title': 'New Book', 'author':
                 'New Author'}
    with patch('src.application.books_services.BooksService.add',
               return_value={
                   'id': 2, **book_data, 'is_borrowed': False,
                   'borrowed_date': None,
                   'borrowed_by': None
               }):
        response = client.post('/books/', json=book_data)
        assert response.status_code == 201
        assert response.json()['title'] == 'New Book'


def test_update_book(client):
    updated_data = {'title': 'Updated', 'author': 'Updated'}
    with patch('src.application.books_services.BooksService.update',
               return_value=True):
        response = client.put('/books/1', json=updated_data)
        assert response.status_code == 200


def test_delete_book(client):
    with patch('src.application.books_services.BooksService.delete',
               return_value=True):
        response = client.delete('/books/1')
        assert response.status_code == 200
