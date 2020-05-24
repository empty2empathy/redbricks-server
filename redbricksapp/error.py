from typing import Any
from flask import jsonify
from werkzeug.exceptions import HTTPException, default_exceptions


class ExceptionBase(HTTPException):
    def __init__(
        self, message: str, payload: Any = None, status_code: int = 500
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def as_response(self) -> Any:
        resp = jsonify(
            {
                "message": self.message,
                "payload": self.payload,
                "status_code": self.status_code,
            }
        )
        resp.status_code = self.status_code
        return resp


def ExceptionApp(app):
    def error_handler(error):
        if isinstance(error, ExceptionBase):
            return error.as_response()
        else:
            resp = jsonify({"code": error.code, "message": str(error.description)})
            resp.status_code = error.code
            return resp

    for code in default_exceptions.keys():
        app.register_error_handler(code, error_handler)
    return app
