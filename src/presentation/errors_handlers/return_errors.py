from fastapi.responses import JSONResponse


class ReturnErrors:
    @staticmethod
    def book_not_found():
        return JSONResponse(status_code=404,
                            content={"error": "Book not found"})

    @staticmethod
    def book_not_borrowed():
        return JSONResponse(status_code=400,
                            content={"error":
                                     "Book is not currently borrowed"})

    @staticmethod
    def failed_to_return():
        return JSONResponse(status_code=500,
                            content={"error": "Failed to return book"})

    @staticmethod
    def unknown_error():
        return JSONResponse(status_code=500,
                            content={"error": "Something went wrong"})
