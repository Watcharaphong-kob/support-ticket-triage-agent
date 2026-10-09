import pytest

from triage_agent.knowledge.database import KnowledgeError
from triage_agent.knowledge.embeddings import FakeEmbedder
from triage_agent.knowledge.postgres_store import PostgresStore
from triage_agent.schemas import KnowledgeArticle


def article(**changes):
    value = dict(
        id="test-billing",
        title="Billing guidance",
        content="Reported payment charges.",
        locale="en",
        product=None,
        issue_type="billing",
        version="1",
        is_mock=True,
    )
    value.update(changes)
    return KnowledgeArticle.model_validate(value)


def test_ingestion_is_idempotent_replaces_stale_chunks_and_preserves_thai(empty_database):
    store = PostgresStore(FakeEmbedder(), empty_database)
    assert store.ingest([article()]) == {"documents": 1, "chunks": 1}
    assert store.ingest([article()]) == {"documents": 1, "chunks": 1}
    changed = article(content="ระบบเข้าไม่ได้ครับ ขึ้น error 500", locale="th", version="2")
    assert store.ingest([changed]) == {"documents": 1, "chunks": 1}
    assert store.stats() == {"documents": 1, "chunks": 1}


def test_embedding_space_mismatch_rejected_without_corrupting_knowledge(empty_database):
    store = PostgresStore(FakeEmbedder(), empty_database)
    store.ingest([article()])
    incompatible = PostgresStore(FakeEmbedder(dimension=32), empty_database)
    with pytest.raises(KnowledgeError, match="embedding space"):
        incompatible.ingest([article(id="other")])
    assert store.stats() == {"documents": 1, "chunks": 1}
