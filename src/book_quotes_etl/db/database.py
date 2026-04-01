import sqlite3

from book_quotes_etl.config.settings import SQLITE_DB
from book_quotes_etl.db.models import create_tables


def get_connection():
    SQLITE_DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(SQLITE_DB)
    create_tables(conn)
    return conn
