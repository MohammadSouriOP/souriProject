from flask import Flask

from src.presentation.views.books_view import BooksView
from src.presentation.views.borrow_view import BorrowView
from src.presentation.views.member_view import MembersView
from src.presentation.views.return_view import ReturnView


def routes(app: Flask):
    books_view = BooksView.as_view('books_view')

    app.add_url_rule('/books', view_func=books_view, methods=['GET', 'POST'])
    app.add_url_rule('/books/<string:book_id>',
                     view_func=books_view, methods=['GET', 'PUT',
                                                    'DELETE', 'PATCH'])

    members_view = MembersView.as_view('members_view')
    app.add_url_rule(
        '/members',
        view_func=members_view,
        methods=['GET', 'POST'])
    app.add_url_rule(
        '/members/<string:member_id>',
        view_func=members_view,
        methods=['GET', 'PUT', 'DELETE', 'PATCH'])

    borrow_view = BorrowView.as_view('borrow_view')
    app.add_url_rule(
        '/borrow/<string:book_id>/<string:member_id>',
        view_func=borrow_view,
        methods=['POST'])

    return_view = ReturnView.as_view('return_view')
    app.add_url_rule(
        '/return/<string:book_id>',
        view_func=return_view,
        methods=['POST'])
