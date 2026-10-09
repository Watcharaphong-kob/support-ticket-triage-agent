import json
from pathlib import Path

import pytest

from triage_agent.agent import Agent
from triage_agent.cli import main
from triage_agent.knowledge.embeddings import FakeEmbedder
from triage_agent.knowledge.postgres_store import PostgresStore
from triage_agent.models import OfflineModel
from triage_agent.schemas import KnowledgeArticle, SearchArguments, Ticket
from triage_agent.tools import ToolDispatcher

ROOT = Path(__file__).resolve().parents[1]


def seed(dsn):
    store = PostgresStore(FakeEmbedder(), dsn)
    store.ingest(
        [
            KnowledgeArticle.model_validate(a)
            for a in json.loads((ROOT / "data/knowledge_base.json").read_text(encoding="utf-8"))
        ]
    )
    return store


def test_three_source_tickets_use_real_database_and_grounded_sources(empty_database):
    store = seed(empty_database)
    agent = Agent(OfflineModel(), ToolDispatcher(ROOT / "data/customers.json", store))
    tickets = [
        Ticket.model_validate(t)
        for t in json.loads((ROOT / "data/sample_tickets.json").read_text(encoding="utf-8"))
    ]
    expected = [
        ("high", "billing_payments", "mock-billing-en"),
        ("critical", "incident_on_call", "mock-access-th"),
        ("low", "product_support", "mock-theme-en"),
    ]
    for ticket, (urgency, destination, source) in zip(tickets, expected, strict=True):
        result = agent.triage(ticket)
        assert result.status == "completed"
        assert result.urgency == urgency
        assert result.destination == destination
        cited = store.search(
            SearchArguments(
                query=next(
                    a["content"]
                    for a in json.loads(
                        (ROOT / "data/knowledge_base.json").read_text(encoding="utf-8")
                    )
                    if a["id"] == source
                )
            )
        )
        assert any(d.id == source and d.chunk_id in result.knowledge_sources for d in cited)
        assert len(result.tool_calls) == 2
        assert all(c.status == "ok" for c in result.tool_calls)
        assert result.product is None
    assert any("\u0e00" <= char <= "\u0e7f" for char in agent.triage(tickets[1]).draft_response)
    assert "scheduled dark mode feature request" in agent.triage(tickets[2]).secondary_issues


def test_cli_batch_stdout_is_json_and_traces_are_stderr(empty_database, monkeypatch, capsys):
    seed(empty_database)
    monkeypatch.setenv("PGOPTIONS", empty_database.split("options=")[1].strip("'"))
    monkeypatch.setenv("EMBEDDING_BACKEND", "fake")
    monkeypatch.setenv("EMBEDDING_MODEL", "fake-token-v1")
    monkeypatch.setenv("EMBEDDING_DIMENSION", "64")
    code = main(
        [
            "--input",
            str(ROOT / "data/sample_tickets.json"),
            "--customers",
            str(ROOT / "data/customers.json"),
            "--offline",
            "--trace",
        ]
    )
    output = capsys.readouterr()
    assert code == 0
    value = json.loads(output.out)
    assert value["mode"] == "offline_demo"
    assert len(value["results"]) == 3
    assert len(output.err.splitlines()) == 3


def test_cli_database_outage_has_json_fallback_and_nonzero_status(monkeypatch, capsys):
    monkeypatch.setenv("PGHOST", "127.0.0.1")
    monkeypatch.setenv("PGPORT", "1")
    monkeypatch.setenv("EMBEDDING_BACKEND", "fake")
    monkeypatch.setenv("EMBEDDING_MODEL", "fake-token-v1")
    monkeypatch.setenv("EMBEDDING_DIMENSION", "64")
    code = main(
        [
            "--input",
            str(ROOT / "data/sample_tickets.json"),
            "--customers",
            str(ROOT / "data/customers.json"),
            "--offline",
        ]
    )
    output = capsys.readouterr()
    assert code == 1
    assert all(r["status"] == "fallback" for r in json.loads(output.out)["results"])


def test_prompt_delivery_copy_matches_installed_resource():
    from importlib.resources import files

    source = ROOT / "prompts/system.txt"
    if not source.exists():
        pytest.skip("Delivery copy checked on host; package prompt exercised in container")
    assert source.read_text(encoding="utf-8") == files("triage_agent").joinpath(
        "prompts/system.txt"
    ).read_text(encoding="utf-8")
