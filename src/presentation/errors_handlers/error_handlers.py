from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from src.presentation.errors_handlers.borrow_errors import BorrowErrors
from src.presentation.errors_handlers.member_errors import MemberErrors


def error_handlers(app: FastAPI):

    @app.exception_handler(404)
    async def not_found(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=404,
            content={"error": "Resource not found"}
        )

    @app.exception_handler(400)
    async def bad_request(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=400,
            content={"error": "Bad request"}
        )

    @app.exception_handler(500)
    async def internal_server_error(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )

    @app.exception_handler(ValueError)
    async def handle_value_error(request: Request, exc: ValueError):
        return BorrowErrors.already_borrowed()

    @app.exception_handler(KeyError)
    async def handle_key_error(request: Request, exc: KeyError):
        return BorrowErrors.book_not_found()

    @app.exception_handler(IntegrityError)
    async def handle_integrity_error(request: Request, exc: IntegrityError):
        if 'duplicate key value violates unique constraint' in str(exc):
            return MemberErrors.email_already_exists()
        return MemberErrors.database_error()

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request,
                                      exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={"error": "Validation error", "details": exc.errors()}
        )

    @app.exception_handler(Exception)
    async def catch_all_errors(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"error": "Unexpected server error", "details": str(exc)}
        )
