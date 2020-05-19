from typing import Any
from flask import make_response, jsonify


class ExceptionBase(Exception):
    def __init__(self, message: str, payload: Any = None, status_code: int = 500) -> None:
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def as_response(self) -> Any:
        return make_response(
            jsonify({
                'message': self.message,
                'payload': self.payload,
                'status_code': self.status_code
            }),
            self.status_code
        )
