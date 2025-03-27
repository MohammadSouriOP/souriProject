from unittest.mock import patch


def test_return_book_success(client):
    with patch('src.application.books_services.BooksService.return_book',
               return_value={
                   'id': 1, 'title': 'Book A',
                   'author': 'Author A',
                   'is_borrowed': False, 'borrowed_date': None,
                   'borrowed_by': None
               }):
        response = client.post('/return/1')
        assert response.status_code == 200
        assert response.json()['is_borrowed'] is False


def test_return_book_not_borrowed(client):
    with patch('src.application.books_services.BooksService.return_book',
               side_effect=ValueError):
        response = client.post('/return/1')
        assert response.status_code == 400
        assert 'error' in response.json()


def test_return_book_not_found(client):
    with patch('src.application.books_services.BooksService.return_book',
               side_effect=KeyError):
        response = client.post('/return/999')
        assert response.status_code == 404
        assert 'error' in response.json()


def test_return_book_failed_update(client):
    with patch('src.application.books_services.BooksService.return_book',
               return_value=None):
        response = client.post('/return/1')
        assert response.status_code == 500
        assert 'error' in response.json()
