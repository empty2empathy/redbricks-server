from typing import Any
from flask import make_response, jsonify


class ErrorResponse:
    def __init__(self, error: Exception, message: str, data: Any, code: int) -> None:
        self.error = error
        self.message = message
        self.code = code

    def as_response(self) -> Any:
        return make_response(
            jsonify({
                'statusCode': self.error,
                'message': self.message
            }),
            self.code
        )
