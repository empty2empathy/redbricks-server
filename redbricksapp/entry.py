from datetime import datetime

from flask import Flask, jsonify
from flask_cors import CORS

from .controllers import BLUEPRINTS
from .handler import RequestClass, ResponseClass
from .modules.database import SessionScope
from .modules.encoder import JSONEncoder
from .error import ExceptionBase


def create_app(
    config_object: object,
    *,
    serve_api: bool = True
):
    class _APP(Flask):
        request_class = RequestClass
        response_class = ResponseClass
        json_encoder = JSONEncoder

        def make_response(self, rv):
            if isinstance(rv, (list, bool, int, *JSONEncoder.__CUSTOM_OBJECT__)):
                rv = jsonify(rv)
            return super().make_response(rv)

        def process_response(self, response):
            response.headers['server'] = 'Awesome Server!'
            return Flask.process_response(app, response)

    app = _APP(__name__)
    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        max_age=31536000,
        supports_credentials=True
    )

    @app.errorhandler(ExceptionBase)
    def response_exception(exception: ExceptionBase):
        return exception.as_response()

    @app.route("/")
    def alive():
        return datetime.now().ctime()

    @app.teardown_request
    def remove_session(exception=None):
        SessionScope.remove()

    if serve_api:
        for blueprint in BLUEPRINTS:
            app.register_blueprint(blueprint)

    app.config.from_object(config_object)
    return app
