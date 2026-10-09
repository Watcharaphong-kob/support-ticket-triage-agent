import json
from pathlib import Path

from triage_agent.knowledge.embeddings import FakeEmbedder
from triage_agent.knowledge.postgres_store import PostgresStore
from triage_agent.schemas import KnowledgeArticle
from triage_agent.tools import TOOL_DEFINITIONS, ToolDispatcher

ROOT = Path(__file__).resolve().parents[1]


def dispatcher(dsn="host=127.0.0.1 port=1 dbname=unavailable"):
    return ToolDispatcher(ROOT / "data/customers.json", PostgresStore(FakeEmbedder(), dsn))


def test_history_unknown_customer_and_allowlisted_argument_validation():
    tools = dispatcher()
    found = tools.call("get_customer_history", {"customer_id": "customer-002"})
    assert found["status"] == "ok" and found["customer"]["seats"] == 45
    assert found["customer"]["is_synthetic"] is True
    assert tools.call("get_customer_history", {"customer_id": "missing"}) == {
        "status": "not_found",
        "customer": None,
        "error": None,
    }
    assert tools.call("get_customer_history", {"customer_id": ""})["status"] == "error"
    assert (
        tools.call("search_knowledge_base", {"query": "x", "sql": "DROP TABLE"})["status"]
        == "error"
    )
    assert tools.call("refund_card", {})["error"] == "unknown_tool"
    assert {d["function"]["name"] for d in TOOL_DEFINITIONS} == {
        "get_customer_history",
        "search_knowledge_base",
    }
    assert all(
        d["function"]["parameters"]["additionalProperties"] is False for d in TOOL_DEFINITIONS
    )


def test_database_failure_is_sanitized_and_never_an_empty_success():
    result = dispatcher().call("search_knowledge_base", {"query": "payment"})
    assert result == {"status": "error", "documents": [], "error": "knowledge_unavailable"}


def test_both_tools_execute_against_real_database_and_empty_matches_are_success(empty_database):
    tools = dispatcher(empty_database)
    docs = json.loads((ROOT / "data/knowledge_base.json").read_text(encoding="utf-8"))
    tools.knowledge.ingest([KnowledgeArticle.model_validate(d) for d in docs])
    found = tools.call(
        "search_knowledge_base", {"query": docs[0]["content"], "issue_type": "billing"}
    )
    assert found["status"] == "ok" and found["documents"][0]["id"] == docs[0]["id"]
    assert found["documents"][0]["is_mock"] is True
    assert tools.call("get_customer_history", {"customer_id": "customer-001"})["status"] == "ok"
    empty = tools.call("search_knowledge_base", {"query": "payment", "product": "not-a-product"})
    assert empty == {"status": "ok", "documents": [], "error": None}
