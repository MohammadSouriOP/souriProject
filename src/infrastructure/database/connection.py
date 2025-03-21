from sqlalchemy import create_engine
from sqlalchemy.engine import Connection, Engine

DATABASE_URL = 'postgresql://souri:souri@localhost:5432/souri_db'

engine: Engine = create_engine(DATABASE_URL, echo=True)


def get_connection() -> Connection:
    return engine.connect()
