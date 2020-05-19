from flask import Blueprint

from ..models import Artist
from ..error import ExceptionBase

testt = Blueprint('test_bp', __name__)


@testt.route('/a')
def testa():
    return Artist.query.first()


@testt.route('/b')
def testb():
    return {"result": Artist.query.first()}


@testt.route('/c')
def testc():
    raise ExceptionBase("this is msg", Artist.query.first(), 500)
