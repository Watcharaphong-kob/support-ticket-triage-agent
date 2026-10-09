"""Bounded PostgreSQL connections and packaged schema initialization."""

from contextlib import contextmanager
from importlib.resources import files

import psycopg
from pgvector.psycopg import register_vector


class KnowledgeError(RuntimeError):
    """Public, sanitized knowledge-system error."""


@contextmanager
def connection(dsn: str = "", *, readonly: bool = False):
    with psycopg.connect(dsn, connect_timeout=5) as conn:
        conn.execute("SET statement_timeout = '5000ms'")
        register_vector(conn)
        conn.commit()
        conn.read_only = readonly
        yield conn


def migrate(dsn: str = "") -> str:
    sql = files("triage_agent.knowledge").joinpath("migrations/001_knowledge.sql").read_text()
    with psycopg.connect(dsn, connect_timeout=5) as conn:
        conn.execute("SET statement_timeout = '5000ms'")
        conn.execute(sql)
        row = conn.execute(
            "SELECT extversion FROM pg_extension WHERE extname = 'vector'"
        ).fetchone()
        return row[0]
