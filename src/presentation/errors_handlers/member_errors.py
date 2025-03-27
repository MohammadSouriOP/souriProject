from fastapi.responses import JSONResponse


class MemberErrors:
    @staticmethod
    def member_not_found():
        return JSONResponse(status_code=404,
                            content={"error": "Member not found"})

    @staticmethod
    def email_already_exists():
        return JSONResponse(status_code=400,
                            content={"error": "Email already exists"})

    @staticmethod
    def database_error():
        return JSONResponse(status_code=500,
                            content={"error": "Database error"})

    @staticmethod
    def unknown_error():
        return JSONResponse(status_code=500,
                            content={"error": "Something went wrong"})

    @staticmethod
    def invalid_uuid():
        return JSONResponse(status_code=400,
                            content={"error": "Invalid UUID format"})
