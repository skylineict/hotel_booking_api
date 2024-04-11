from rest_framework.exceptions import APIException


class CustomException(APIException):
    """ Custom Exception Handler """
    def __init__(self, detail, code):
        super().__init__(detail, code)
        if "errors" in detail and isinstance(detail["errors"], dict):
            detail["message"] = detail["errors"][next(iter(detail["errors"]))][0]

        self.detail = detail
        self.status_code = code