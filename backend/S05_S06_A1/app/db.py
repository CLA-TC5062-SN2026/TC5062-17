from contextlib import contextmanager
from typing import Iterator

import psycopg
from psycopg import Connection
from psycopg.rows import dict_row

from .config import get_settings


@contextmanager
def connection() -> Iterator[Connection]:
    with psycopg.connect(get_settings().database_url, row_factory=dict_row) as conn:
        yield conn


def check_connection() -> str:
    with connection() as conn:
        row = conn.execute("SELECT current_database() AS db, version() AS version").fetchone()
        return f"{row['db']} | {row['version']}"
