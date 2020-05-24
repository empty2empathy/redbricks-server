import textwrap
from contextlib import contextmanager
from typing import Any, ContextManager, Optional, Callable

from flask import _app_ctx_stack, abort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.session import Session as SessionBase
from sqlalchemy.orm.query import Query as QueryBase
from sqlalchemy.ext.declarative import declarative_base

from ..config import connection_string, ENV
from ..error import ExceptionBase
from .pagination import Pagination
from .serializable import SerializableMixin


class SessionKlass(SessionBase):
    ...


class QueryKlass(QueryBase):
    def paginate(self, page: int = 1, page_unit: int = 20) -> Pagination:
        return Pagination(self, page, page_unit)

    def get_or_404(
        self, ident: Any, description: str = None, error: ExceptionBase = None
    ) -> Any:
        item = self.get(ident)
        if item is None:
            if ExceptionBase:
                raise error
            else:
                abort(404, description=description)
        else:
            return item

    def first_or_404(self, description: str = None, error: ExceptionBase = None):
        item = self.first()
        if item is None:
            if ExceptionBase:
                raise error
            else:
                abort(404, description=description)
        return item


class BaseKlass(SerializableMixin):
    def to_dict(self, mapper: Optional[Callable[[Any], Any]] = None) -> dict:
        """dict 형식으로 변환합니다."""

        if not mapper:
            return self.serialize()
        else:
            from .mapper import __all__ as all_mappers

            m = mapper() if mapper in all_mappers else mapper
            return m(self)

    def __repr__(self):
        """엔티티의 속성을 표시합니다."""
        cols = ", ".join(
            col.key
            + "="
            + textwrap.shorten(
                repr(getattr(self, col.key)), width=16, placeholder="..."
            )
            for col in self.__table__.c
        )
        return f"<{type(self).__name__}: {self.__tablename__}, [{cols}]>"

    def __iter__(self):
        """(컬럼명, 값) 튜플을 제공하는 이터레이터를 반환합니다."""
        for c in self.__table__.c:
            yield (c.key, getattr(self, c.key))

    def __getitem__(self, key):
        if key in self.__table__.c:
            return getattr(self, key)
        else:
            raise KeyError(f"Unknown Column Name: {key}")

    def __setitem__(self, key, item):
        if key in self.__table__.c:
            setattr(self, key, item)
        else:
            raise KeyError(f"Unknown Column Name: {key}")


engine = create_engine(
    connection_string,
    pool_recycle=3600,
    pool_size=20,
    max_overflow=5,
    encoding="utf-8",
    echo=(ENV == "local"),
)
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

Base: BaseKlass = declarative_base(cls=BaseKlass, name=BaseKlass.__name__)
Base.query = SessionScope.query_property()


@contextmanager
def Session() -> ContextManager[SessionKlass]:
    session = SessionScope()
    try:
        yield session
        session.commit()
        session.expunge_all()
        session.expire_all()
    except Exception as exc:
        session.rollback()
        raise exc
    finally:
        session.close()


def SessionApp(app):
    def remove_session(exception=None):
        SessionScope.remove()

    app.teardown_request(remove_session)
