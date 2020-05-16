from flask import Request, Response, jsonify, request
from .error import ErrorResponse


class RequestClass(Request):
    def __init__(self, *args, **kwargs):
        super(RequestClass, self).__init__(*args, **kwargs)


class ResponseClass(Response):
    charset = 'utf-8'
    default_status = 200
    default_mimetype = 'application/json'

    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, (dict, list, str, int, float, bool)):
            rv = jsonify(rv)
        elif isinstance(rv, ErrorResponse):
            rv = rv.as_response()
        return super(ResponseClass, cls).force_type(rv, environ)


request: RequestClass = request  # noqa
