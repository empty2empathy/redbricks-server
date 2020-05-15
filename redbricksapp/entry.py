from datetime import datetime

from flask import Flask, request
from flask_cors import CORS
from simplejson import JSONEncoder

from .handler import ServeRequest, ServeResponse
from .controllers import BLUEPRINTS
from .modules.database import ScopedSession


def create_app(
    config_object: object,
    *,
    serve_api: bool = True
):
    application = Flask(__name__)
    CORS(application, max_age=31536000, supports_credentials=True)
    application.logger.propagate = True

    application.request_class = ServeRequest
    application.response_class = ServeResponse
    application.json_encoder = JSONEncoder

    @application.route("/")
    def alive():
        return datetime.now().ctime()

    @application.teardown_request
    def teardown_request(_):
        ScopedSession.remove()

    if serve_api:
        for blueprint in BLUEPRINTS:
            application.register_blueprint(blueprint)

    application.config.from_object(config_object)
    return application
