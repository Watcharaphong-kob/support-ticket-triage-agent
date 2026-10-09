import json
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest
from fastapi.testclient import TestClient
from test_agent import ROOT, ScriptedChatModel
from test_end_to_end import SampleChatModel

from triage_agent.api import app
from triage_agent.config import Settings


def client():
    return TestClient(app)


def samples():
    return json.loads((ROOT / "data/sample_tickets.json").read_text(encoding="utf-8"))


def test_api_returns_same_envelope_as_cli(empty_database, monkeypatch, capsys):
    from test_end_to_end import seed

    from triage_agent.cli import main

    seed(empty_database)
    monkeypatch.setenv("PGOPTIONS", empty_database.split("options=")[1].strip("'"))
    monkeypatch.setenv("EMBEDDING_BACKEND", "fake")
    monkeypatch.setenv("EMBEDDING_MODEL", "fake-token-v1")
    monkeypatch.setenv("EMBEDDING_DIMENSION", "64")
    monkeypatch.setattr(Settings, "chat_model", lambda self: SampleChatModel())
    response = client().post("/triage", json=samples())
    assert response.status_code == 200
    assert main(["--input", str(ROOT / "data/sample_tickets.json")]) == 0
    assert response.json() == json.loads(capsys.readouterr().out)


def test_api_valid_ticket_requires_config_but_health_is_only_liveness(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    api = client()
    assert api.get("/health").json() == {"status": "alive"}
    response = api.post("/triage", json=samples()[0])
    assert response.status_code == 503
    assert response.json() == {"detail": "Runtime configuration unavailable."}


@pytest.mark.parametrize(
    "payload",
    [
        [],
        {},
        [samples()[0], samples()[0]],
        [samples()[0]] * 101,
        [samples()[0], dict(samples()[1], locale="invalid")],
    ],
)
def test_invalid_requests_execute_neither_model_nor_tools(payload, monkeypatch):
    def forbidden_provider(self):
        raise AssertionError("Invalid request must not construct provider")

    monkeypatch.setattr(Settings, "chat_model", forbidden_provider)
    assert client().post("/triage", json=payload).status_code == 422


def test_malformed_json_is_rejected_before_provider(monkeypatch):
    monkeypatch.setattr(Settings, "chat_model", lambda self: pytest.fail("Provider executed"))
    response = client().post(
        "/triage",
        content="{broken",
        headers={
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 422


def test_accepted_single_ticket_reports_fallback_in_200_response(monkeypatch):
    monkeypatch.setenv("EMBEDDING_BACKEND", "fake")
    monkeypatch.setenv("EMBEDDING_MODEL", "fake-token-v1")
    monkeypatch.setenv("EMBEDDING_DIMENSION", "64")
    monkeypatch.setattr(
        Settings,
        "chat_model",
        lambda self: ScriptedChatModel(turns=[RuntimeError("private provider detail")]),
    )
    response = client().post("/triage", json=samples()[1])
    assert response.status_code == 200
    result = response.json()["results"][0]
    assert result["ticket_id"] == "ticket-002"
    assert result["status"] == "fallback"
    assert result["error"]["code"] == "model_unavailable"
    assert "private" not in response.text


def test_concurrent_requests_keep_customer_and_tool_evidence_isolated(empty_database, monkeypatch):
    from test_end_to_end import seed

    seed(empty_database)
    monkeypatch.setenv("PGOPTIONS", empty_database.split("options=")[1].strip("'"))
    monkeypatch.setenv("EMBEDDING_BACKEND", "fake")
    monkeypatch.setenv("EMBEDDING_MODEL", "fake-token-v1")
    monkeypatch.setenv("EMBEDDING_DIMENSION", "64")
    barrier = Barrier(2)

    class ConcurrentModel(SampleChatModel):
        def _generate(self, messages, **kwargs):
            if messages[-1].type == "human":
                barrier.wait(timeout=10)
            return super()._generate(messages, **kwargs)

    monkeypatch.setattr(Settings, "chat_model", lambda self: ConcurrentModel())
    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(lambda t: client().post("/triage", json=t), samples()[:2]))
    for index, response in enumerate(responses):
        assert response.status_code == 200
        result = response.json()["results"][0]
        assert result["ticket_id"] == samples()[index]["ticket_id"]
        assert result["status"] == "completed"
        assert len(result["tool_calls"]) == 2
        if index == 1:
            assert "รับทราบปัญหา" in result["draft_response"]
