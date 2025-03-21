from flask import jsonify


class BorrowErrors:

    @staticmethod
    def already_borrowed():
        return jsonify({
            'error': 'This book is already borrowed by another member.'}), 400

    @staticmethod
    def book_not_found():
        return jsonify({'error': 'Book not found'}), 404

    @staticmethod
    def member_not_found():
        return jsonify({'error': 'Member not found'}), 404

    @staticmethod
    def database_error():
        return jsonify({'error': 'Database error'}), 500

    @staticmethod
    def unknown_error():
        return jsonify({'error': 'Something went wrong'}), 500


def handle_borrow_errors(error):
    if isinstance(error, ValueError):
        return BorrowErrors.already_borrowed()

    return BorrowErrors.unknown_error()
