import pytest

from triage_agent.knowledge.database import KnowledgeError
from triage_agent.knowledge.embeddings import FakeEmbedder
from triage_agent.knowledge.postgres_store import PostgresStore
from triage_agent.schemas import KnowledgeArticle, SearchArguments


def test_search_returns_bounded_cited_bilingual_evidence_and_applies_filters(empty_database):
    store = PostgresStore(FakeEmbedder(), empty_database)
    articles = [
        KnowledgeArticle(
            id=f"article-{i}",
            title="ระบบ error 500",
            content="ระบบเข้าไม่ได้ครับ ขึ้น error 500",
            locale="th",
            product="example",
            issue_type="service_access",
            version="1",
            is_mock=True,
        )
        for i in range(8)
    ]
    store.ingest(articles)
    found = store.search(SearchArguments(query=articles[0].content, locale="th", product="example"))
    assert len(found) == 5
    assert all(d.id in {a.id for a in articles} and d.is_mock and d.chunk_id for d in found)
    assert found[0].excerpt == articles[0].content
    assert store.search(SearchArguments(query="error 500", locale="en")) == []
    assert (
        store.search(SearchArguments(query="error 500", product="'; DROP TABLE kb_documents; --"))
        == []
    )
    assert store.stats()["documents"] == 8


def test_changed_source_is_searchable_with_new_version_and_no_stale_excerpts(empty_database):
    store = PostgresStore(FakeEmbedder(), empty_database)
    original = KnowledgeArticle(
        id="a",
        title="Billing",
        content="old content",
        locale="en",
        product=None,
        issue_type="billing",
        version="1",
        is_mock=True,
    )
    store.ingest([original])
    new = original.model_copy(update={"content": "replacement payment guidance", "version": "2"})
    store.ingest([new])
    found = store.search(SearchArguments(query=new.content, issue_type="billing"))
    assert len(found) == 1 and found[0].version == "2"
    assert found[0].excerpt == new.content


def test_search_dimension_mismatch_is_not_an_empty_match(empty_database):
    store = PostgresStore(FakeEmbedder(), empty_database)
    store.ingest([])
    with pytest.raises(KnowledgeError, match="embedding space"):
        PostgresStore(FakeEmbedder(32), empty_database).search(SearchArguments(query="payment"))


def test_database_connection_failure_is_explicit():
    with pytest.raises(KnowledgeError, match="unavailable"):
        PostgresStore(FakeEmbedder(), "host=127.0.0.1 port=1 dbname=unavailable").search(
            SearchArguments(query="payment")
        )
