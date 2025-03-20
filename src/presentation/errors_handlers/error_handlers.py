from flask import jsonify
from sqlalchemy.exc import IntegrityError
from src.presentation.errors_handlers.borrow_errors import BorrowErrors
from src.presentation.errors_handlers.member_errors import MemberErrors


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

    def handle_integrity_error(error):
        if "duplicate key value violates unique constraint" in str(error):
            return MemberErrors.email_already_exists()
        return MemberErrors.database_error()

    app.register_error_handler(IntegrityError, handle_integrity_error)

    app.register_error_handler(404, not_found)
