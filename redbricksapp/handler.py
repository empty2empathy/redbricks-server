from flask import Request, Response, jsonify, request
from typing import cast

from .error import ErrorResponse


class ServeRequest(Request):
    def __init__(self, *args, **kwargs):
        super(ServeRequest, self).__init__(*args, **kwargs)


class ServeResponse(Response):
    charset = 'utf-8'
    default_status = 200
    default_mimetype = 'application/json'

    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, (str, int, dict, list)):
            rv = jsonify(rv)
        elif isinstance(rv, ErrorResponse):
            rv = rv.as_response()
        return super(ServeResponse, cls).force_type(rv, environ)


request: ServeRequest = cast(ServeRequest, request)  # noqa
