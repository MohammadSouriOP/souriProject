from fastapi.responses import JSONResponse


class BorrowErrors:
    @staticmethod
    def already_borrowed():
        return JSONResponse(
            status_code=400,
            content={"error":
                     "This book is already borrowed by another member."}
        )

    @staticmethod
    def book_not_found():
        return JSONResponse(status_code=404,
                            content={"error": "Book not found"})

    @staticmethod
    def member_not_found():
        return JSONResponse(status_code=404,
                            content={"error": "Member not found"})

    @staticmethod
    def database_error():
        return JSONResponse(status_code=500,
                            content={"error": "Database error"})

    @staticmethod
    def unknown_error():
        return JSONResponse(status_code=500,
                            content={"error": "Something went wrong"})


def handle_borrow_errors(error):
    if isinstance(error, ValueError):
        return BorrowErrors.already_borrowed()
    return BorrowErrors.unknown_error()
