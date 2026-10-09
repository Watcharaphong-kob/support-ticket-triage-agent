import os
import uuid

import pytest


@pytest.fixture
def fake_embeddings(monkeypatch):
    monkeypatch.setenv("EMBEDDING_BACKEND", "fake")
    monkeypatch.setenv("EMBEDDING_MODEL", "fake-token-v1")
    monkeypatch.setenv("EMBEDDING_DIMENSION", "64")


@pytest.fixture(scope="session")
def database_dsn():
    if os.environ.get("TRIAGE_TEST_DATABASE") != "1":
        pytest.skip("Set TRIAGE_TEST_DATABASE=1 for isolated real PostgreSQL integration tests")
    import psycopg
    from psycopg import sql
    from psycopg.conninfo import make_conninfo

    from triage_agent.knowledge.database import migrate

    schema = "triage_test_" + uuid.uuid4().hex
    with psycopg.connect(autocommit=True) as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        conn.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema)))
    dsn = make_conninfo(options=f"-c search_path={schema},public")
    migrate(dsn)
    try:
        yield dsn
    finally:
        with psycopg.connect(autocommit=True) as conn:
            conn.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema)))


@pytest.fixture
def empty_database(database_dsn):
    from triage_agent.knowledge.database import connection

    with connection(database_dsn) as conn:
        conn.execute("TRUNCATE kb_chunks, kb_documents, kb_space")
    return database_dsn
