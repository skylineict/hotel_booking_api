from rest_framework.exceptions import APIException
from rest_framework.response import Response


class CustomException(APIException):
    """ Custom Exception Handler """

    def __init__(self, detail, code):
        super().__init__(detail, code)
        if isinstance(detail, dict):
            res = {}
            res["message"] = detail[next(iter(detail))][0]
            res["errors"] = detail
        else:
            res["message"] = detail

        res["status"] = "error"
        self.detail = res
        self.status_code = code


class CustomResponse(Response):
    """ Custom Response Handler """

    def __init__(self, detail=None, code=None):
        if code is None:
            code = 200
        if detail is None:
            detail = {"status": "success", "message": "Request was successful"}
        super().__init__(detail, code)
