from sqlalchemy import create_engine, declarative_base, sessionmaker
from contextlib import contextmanager
from ..config import connection_string

Base = declarative_base()
engine = create_engine(connection_string)
Session_ = sessionmaker(bind=engine)


@contextmanager
def Session():
    session = Session_()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()