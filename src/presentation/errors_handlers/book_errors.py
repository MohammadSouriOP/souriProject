from flask import jsonify


class BookErrors:
    @staticmethod
    def book_not_found():
        return jsonify({'error': 'Book not found'}), 404

    @staticmethod
    def book_already_borrowed():
        return jsonify({'error': 'Book is already borrowed.'}), 400

    @staticmethod
    def book_not_borrowed():
        return jsonify({'error': 'Book is not borrowed.'}), 400

    @staticmethod
    def database_error():
        return jsonify({'error': 'Database error'}), 500

    @staticmethod
    def unknown_error():
        return jsonify({'error': 'Something went wrong'}), 500
