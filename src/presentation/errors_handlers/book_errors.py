from fastapi.responses import JSONResponse


class BookErrors:
    @staticmethod
    def book_not_found():
        return JSONResponse(status_code=404,
                            content={"error": "Book not found"})

    @staticmethod
    def book_already_borrowed():
        return JSONResponse(status_code=400,
                            content={"error": "Book is already borrowed."})

    @staticmethod
    def book_not_borrowed():
        return JSONResponse(status_code=400,
                            content={"error": "Book is not borrowed."})

    @staticmethod
    def database_error():
        return JSONResponse(status_code=500,
                            content={"error": "Database error"})

    @staticmethod
    def unknown_error():
        return JSONResponse(status_code=500,
                            content={"error": "Something went wrong"})
