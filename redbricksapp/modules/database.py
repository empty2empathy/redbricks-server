import textwrap
from contextlib import contextmanager

from flask import _app_ctx_stack
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.session import Session as SessionBase
from sqlalchemy.orm.query import Query as QueryBase
from sqlalchemy.ext.declarative import declarative_base

from ..config import connection_string
from .pagination import Pagination


class SessionKlass(SessionBase):
    ...


class QueryKlass(QueryBase):
    def paginate(self, page: int = 1, page_unit: int = 20) -> Pagination:
        return Pagination(self, page, page_unit)


class BaseKlass:
    def __repr__(self):
        """엔티티의 속성을 표시합니다."""
        cols = ", ".join(col.key + "=" + textwrap.shorten(repr(getattr(self, col.key)), width=16, placeholder="...") for col in self.__table__.c)
        return f"<{type(self).__name__}: {self.__tablename__}, [{cols}]>"

    def __iter__(self):
        """(컬럼명, 값) 튜플을 제공하는 이터레이터를 반환합니다."""
        for c in self.__table__.c:
            yield (c.key, getattr(self, c.key))

    def __getitem__(self, key):
        if key in self.__table__.c:
            return getattr(self, key)
        else:
            raise KeyError(f'Unknown Column Name: {key}')

    def __setitem__(self, key, item):
        if key in self.__table__.c:
            setattr(self, key, item)
        else:
            raise KeyError(f'Unknown Column Name: {key}')


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
