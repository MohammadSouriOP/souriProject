from flask import jsonify

from src.presentation.errors_handlers.borrow_errors import BorrowErrors


def error_handlers(app):

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"error": "Internal server error"}), 500

    app.register_error_handler(ValueError, BorrowErrors.already_borrowed)
    app.register_error_handler(KeyError, BorrowErrors.book_not_found)

    app.register_error_handler(404, not_found)
