from datetime import datetime

from flask import Flask, jsonify
from flask_cors import CORS
from simplejson import JSONEncoder

from .handler import RequestClass, ResponseClass
from .controllers import BLUEPRINTS
from .modules.database import SessionScope


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
            if isinstance(rv, (list, bool, int)):
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
