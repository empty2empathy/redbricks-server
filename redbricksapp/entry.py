from json import JSONEncoder

from flask import Flask, jsonify, request
from flask_cors import CORS

from .handler import ServeRequest, ServeResponse
from .controllers import BLUEPRINTS
from .modules.database import ScopedSession


def create_app(
    config_object: object,
    *,
    serve_api: bool = True
):
    """Flask WSGI 앱 생성

    Flask WSGI 앱을 생성합니다.

    Args:
        config_object: 설정 객체입니다
        serve_api: 서비스 API 제공 여부\

    Returns:
        Flask Application
    """

    application = Flask(__name__)
    CORS(application, max_age=31536000, supports_credentials=True)
    application.logger.propagate = True

    application.request_class = ServeRequest
    application.response_class = ServeResponse
    application.json_encoder = JSONEncoder

    # ELB Health Check Route
    @application.route("/")
    @application.route("/alive")
    def status():
        return request.base_url + " alive"

    @application.teardown_request
    def teardown_request(_):
        ScopedSession.remove()

    if serve_api:
        for blueprint in BLUEPRINTS:
            application.register_blueprint(blueprint)

    application.config.from_object(config_object)
    return application
