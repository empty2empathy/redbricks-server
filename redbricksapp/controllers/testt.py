from flask import Blueprint

testt = Blueprint('test_bp', __name__)


@testt.route('/<int:page>')
def returnok(page):
    1
