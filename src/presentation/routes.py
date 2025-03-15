from flask import Flask

from src.presentation.views.books_view import BooksView


def routes(app: Flask):
    books_view = BooksView.as_view('books_view')

    app.add_url_rule('/books', view_func=books_view, methods=['GET', 'POST'])
    app.add_url_rule('/books/<int:book_id>',
                     view_func=books_view, methods=['GET', 'PUT', 'DELETE'])

    # borrow_view = BorrowView.as_view('borrow_view')
    # app.add_url_rule('/borrow/<int:book_id>/<int:member_id>',
    # view_func=borrow_view, methods=['POST'])

    # return_view = returnView.as_view('return_view')
    # app.add_url_rule('/return/<int:book_id>',
    #  view_func=return_view, methods=['POST'])

    # members_view = membersView.as_view('members_view')
    # app.add_url_rule('/members', view_func=members_view,
    # methods=['GET', 'POST'])
    # app.add_url_rule('/members/<int:member_id>',
    # view_func=members_view, methods=['GET', 'PUT', 'DELETE'])
