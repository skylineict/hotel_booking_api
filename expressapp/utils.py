from rest_framework.response import Response


class CustomException(Response):
    """Custom Exception Handler"""

    def __init__(self, detail, code):
        if isinstance(detail, dict):
            res = {
                "status": "error",
                "message": detail[next(iter(detail))][0],
                "error": detail,
            }
        else:
            res = {
                "status": "error",
                "message": detail,
            }
        super().__init__(res, code)


class CustomResponse(Response):
    """Custom Response Handler"""

    def __init__(
        self,
        data: any,
        message: str = "Request successful",
        status_code: int = 200,
    ):
        res = {
            "status": "success",
            "message": message,
            "data": data,
        }
        super().__init__(res, status=status_code)
