from datetime import datetime

from flask import Flask, jsonify
from flask_cors import CORS

from .controllers import RegisterBlurprint
from .handler import RequestClass, ResponseClass
from .modules.database import SessionApp
from .modules.encoder import JSONEncoder
from .error import ExceptionApp


def create_app(config_object: object, *, serve_api: bool = True):
    class _APP(Flask):
        request_class = RequestClass
        response_class = ResponseClass
        json_encoder = JSONEncoder

        def make_response(self, rv):
            if isinstance(rv, (list, bool, int, *JSONEncoder.__CUSTOM_OBJECT__)):
                rv = jsonify(rv)
            return super().make_response(rv)

        def process_response(self, response):
            response.headers["server"] = "Awesome Server!"
            return Flask.process_response(app, response)

    app = _APP(__name__)
    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        max_age=31536000,
        supports_credentials=True,
    )
    ExceptionApp(app)
    SessionApp(app)

    @app.route("/")
    def alive():
        return datetime.now().ctime()

    if serve_api:
        app = RegisterBlurprint(app)

    app.config.from_object(config_object)
    return app
