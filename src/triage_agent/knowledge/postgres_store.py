"""Small-corpus classic RAG using PostgreSQL and exact pgvector similarity."""

import psycopg
from pgvector import Vector

from triage_agent.knowledge.database import KnowledgeError, connection
from triage_agent.knowledge.embeddings import Embedder, validate_vectors
from triage_agent.knowledge.ingest import content_hash, prepare_articles
from triage_agent.schemas import KnowledgeArticle, KnowledgeDocument, SearchArguments


class PostgresStore:
    def __init__(self, embedder: Embedder, dsn: str = ""):
        self.embedder, self.dsn = embedder, dsn

    def _check_space(self, conn, *, initialize=False):
        expected = (self.embedder.model, self.embedder.dimension, self.embedder.index_version)
        if initialize:
            conn.execute("SELECT pg_advisory_xact_lock(73524019)")
            conn.execute(
                "INSERT INTO kb_space VALUES (1, %s, %s, %s) ON CONFLICT DO NOTHING", expected
            )
        row = conn.execute("SELECT model, dimension, index_version FROM kb_space").fetchone()
        if row is None and not initialize:
            return False
        if row != expected:
            raise KnowledgeError("Incompatible embedding space; use a separate database/rebuild")
        return True

    def ingest(self, articles: list[KnowledgeArticle]) -> dict[str, int]:
        prepared = prepare_articles(articles, self.embedder)
        total = 0
        try:
            with connection(self.dsn) as conn:
                self._check_space(conn, initialize=True)
                for item in prepared:
                    article = item.article
                    conn.execute(
                        """INSERT INTO kb_documents VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                        ON CONFLICT (id) DO UPDATE SET title=EXCLUDED.title, locale=EXCLUDED.locale,
                        product=EXCLUDED.product, issue_type=EXCLUDED.issue_type,
                        version=EXCLUDED.version, is_mock=EXCLUDED.is_mock,
                        content_hash=EXCLUDED.content_hash""",
                        (
                            article.id,
                            article.title,
                            article.locale,
                            article.product,
                            article.issue_type,
                            article.version,
                            article.is_mock,
                            content_hash(article.content),
                        ),
                    )
                    conn.execute("DELETE FROM kb_chunks WHERE document_id=%s", (article.id,))
                    for sequence, (text, vector) in enumerate(zip(item.chunks, item.vectors)):
                        chunk_id = content_hash(f"{article.id}:{sequence}:{content_hash(text)}")
                        conn.execute(
                            "INSERT INTO kb_chunks VALUES (%s,%s,%s,%s,%s,%s,%s)",
                            (
                                chunk_id,
                                article.id,
                                sequence,
                                text,
                                content_hash(text),
                                Vector(vector),
                                self.embedder.dimension,
                            ),
                        )
                    total += len(item.chunks)
            return {"documents": len(articles), "chunks": total}
        except psycopg.Error as exc:
            raise KnowledgeError("Knowledge database ingestion failed") from exc

    def stats(self) -> dict[str, int]:
        try:
            with connection(self.dsn, readonly=True) as conn:
                documents = conn.execute("SELECT count(*) FROM kb_documents").fetchone()[0]
                chunks = conn.execute("SELECT count(*) FROM kb_chunks").fetchone()[0]
                return {"documents": documents, "chunks": chunks}
        except psycopg.Error as exc:
            raise KnowledgeError("Knowledge database unavailable") from exc

    def search(self, arguments: SearchArguments) -> list[KnowledgeDocument]:
        vectors = self.embedder.embed([arguments.query])
        validate_vectors(vectors, 1, self.embedder.dimension)
        try:
            with connection(self.dsn, readonly=True) as conn:
                if not self._check_space(conn):
                    return []
                rows = conn.execute(
                    """SELECT d.id, c.id, d.title, c.text, d.locale, d.version, d.is_mock,
                    1 - (c.embedding <=> %s) AS score
                    FROM kb_chunks c JOIN kb_documents d ON d.id=c.document_id
                    WHERE (%s::text IS NULL OR d.product=%s)
                    AND (%s::text IS NULL OR d.issue_type=%s)
                    AND (%s::text IS NULL OR d.locale=%s)
                    AND 1 - (c.embedding <=> %s) >= 0.2
                    ORDER BY c.embedding <=> %s, d.id, c.sequence LIMIT 5""",
                    (
                        Vector(vectors[0]),
                        arguments.product,
                        arguments.product,
                        arguments.issue_type,
                        arguments.issue_type,
                        arguments.locale,
                        arguments.locale,
                        Vector(vectors[0]),
                        Vector(vectors[0]),
                    ),
                ).fetchall()
                return [
                    KnowledgeDocument(
                        id=r[0],
                        chunk_id=r[1],
                        title=r[2],
                        excerpt=r[3],
                        locale=r[4],
                        version=r[5],
                        is_mock=r[6],
                        score=float(r[7]),
                    )
                    for r in rows
                ]
        except psycopg.Error as exc:
            raise KnowledgeError("Knowledge database unavailable") from exc
