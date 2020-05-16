from contextlib import contextmanager

from flask import _app_ctx_stack
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.session import Session as SessionBase
from sqlalchemy.orm.query import Query as QueryBase
from sqlalchemy.ext.declarative import declarative_base

from ..config import connection_string


class SessionKlass(SessionBase):
    ...


class QueryKlass(QueryBase):
    ...


class BaseKlass:
    ...


engine = create_engine(connection_string)
SessionScope = scoped_session(
    sessionmaker(
        class_=SessionKlass,
        autocommit=False,
        autoflush=False,
        bind=engine,
        query_cls=QueryKlass,
    ),
    scopefunc=_app_ctx_stack.__ident_func__,
)

Base = declarative_base(cls=BaseKlass, name="BaseKlass")
Base.query = SessionScope.query_property()


@contextmanager
def Session() -> SessionKlass:
    session = SessionScope()
    try:
        yield session
        session.commit()
    except Exception as exc:
        session.rollback()
        raise
    finally:
        session.close()
