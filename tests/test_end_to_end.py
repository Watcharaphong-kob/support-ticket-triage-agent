import json
from pathlib import Path

import pytest
from langchain_core.outputs import ChatGeneration, ChatResult
from test_agent import ScriptedChatModel, decision, tool_requests

from triage_agent.agent import Agent
from triage_agent.cli import main
from triage_agent.config import Settings
from triage_agent.knowledge.embeddings import FakeEmbedder
from triage_agent.knowledge.postgres_store import PostgresStore
from triage_agent.schemas import KnowledgeArticle, SearchArguments, Ticket
from triage_agent.tools import ToolDispatcher

ROOT = Path(__file__).resolve().parents[1]


class SampleChatModel(ScriptedChatModel):
    """Three literal sample decisions for wiring tests, never a GPT quality benchmark."""

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        self.observed.append(list(messages))
        current = json.loads(messages[1].content)
        index = current["source_sample"] - 1
        outputs = [json.loads(m.content) for m in messages if m.type == "tool"]
        if not outputs:
            response = tool_requests(current["customer_id"])
            response.tool_calls[1]["args"]["query"] = [
                "payment failed Pro charges",
                "ระบบเข้าไม่ได้ error 500 demo",
                "System Default dark theme scheduling",
            ][index]
        else:
            urgency, issue, destination, sentiment, draft = [
                ("high", "billing", "billing_payments", "angry", "Billing review needed."),
                (
                    "critical",
                    "service_access",
                    "incident_on_call",
                    "frustrated",
                    "รับทราบปัญหา error 500 ต้องให้ทีม incident ตรวจสอบ ยังไม่ยืนยันเวลาซ่อม",
                ),
                ("low", "theme", "product_support", "mixed", "Product investigation needed."),
            ][index]
            response = decision(
                ticket_id=current["ticket_id"],
                urgency=urgency,
                issue_type=issue,
                destination=destination,
                customer_sentiment=sentiment,
                draft_response=draft,
                next_action="route_to_specialist" if index == 2 else "escalate_to_human",
                secondary_issues=["scheduled dark mode feature request"] if index == 2 else [],
                knowledge_sources=[d["chunk_id"] for o in outputs for d in o.get("documents", [])],
            )
        return ChatResult(generations=[ChatGeneration(message=response)])


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
    agent = Agent(SampleChatModel(), ToolDispatcher(ROOT / "data/customers.json", store))
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
    monkeypatch.setattr(Settings, "chat_model", lambda self: SampleChatModel())
    code = main(
        [
            "--input",
            str(ROOT / "data/sample_tickets.json"),
            "--customers",
            str(ROOT / "data/customers.json"),
            "--trace",
        ]
    )
    output = capsys.readouterr()
    assert code == 0
    value = json.loads(output.out)
    # Runtime contract; injected test model is not live evidence.
    assert value["mode"] == "live_gpt"
    assert len(value["results"]) == 3
    assert len(output.err.splitlines()) == 3


def test_cli_database_outage_has_json_fallback_and_nonzero_status(monkeypatch, capsys):
    monkeypatch.setenv("PGHOST", "127.0.0.1")
    monkeypatch.setenv("PGPORT", "1")
    monkeypatch.setenv("EMBEDDING_BACKEND", "fake")
    monkeypatch.setenv("EMBEDDING_MODEL", "fake-token-v1")
    monkeypatch.setenv("EMBEDDING_DIMENSION", "64")
    monkeypatch.setattr(Settings, "chat_model", lambda self: SampleChatModel())
    code = main(
        [
            "--input",
            str(ROOT / "data/sample_tickets.json"),
            "--customers",
            str(ROOT / "data/customers.json"),
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
