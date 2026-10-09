import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from triage_agent.schemas import Ticket, TriageResult


def test_all_fixture_messages_validate_without_losing_thai():
    path = Path(__file__).resolve().parents[1] / "data/sample_tickets.json"
    tickets = [Ticket.model_validate(t) for t in json.loads(path.read_text(encoding="utf-8"))]
    assert len(tickets[1].messages) == 4
    assert tickets[1].messages[0].text == "ระบบเข้าไม่ได้ครับ ขึ้น error 500"
    assert tickets[1].messages[0].supplied_translation


def result(**changes):
    value = dict(
        ticket_id="ticket-001",
        status="completed",
        urgency="high",
        product=None,
        issue_type="billing",
        customer_sentiment="angry",
        secondary_issues=[],
        next_action="escalate_to_human",
        destination="billing_payments",
        rationale="Reported charges",
        draft_response=None,
        knowledge_sources=[],
        uncertainties=["Charge settlement unknown"],
        tool_calls=[
            {"name": "get_customer_history", "call_id": "1", "status": "ok"},
            {"name": "search_knowledge_base", "call_id": "2", "status": "ok"},
        ],
        error=None,
    )
    value.update(changes)
    return value


def test_completed_result_keeps_unknown_product_and_secondary_issues():
    assert TriageResult.model_validate(result(secondary_issues=["export access"])).product is None


@pytest.mark.parametrize(
    "changes",
    [
        {"urgency": "urgent"},
        {"product": 42},
        {"tool_calls": []},
        {"urgency": None},
        {"next_action": "auto_respond", "destination": "billing_payments"},
        {
            "urgency": "critical",
            "next_action": "route_to_specialist",
            "destination": "technical_support",
        },
        {"unexpected": True},
        {"error": {"code": "oops", "message": "bad"}},
    ],
)
def test_invalid_or_contradictory_completed_results_are_rejected(changes):
    with pytest.raises(ValidationError):
        TriageResult.model_validate(result(**changes))


def test_technical_fallback_allows_unknown_urgency_and_requires_human_support():
    changes = dict(
        status="fallback",
        urgency=None,
        issue_type=None,
        tool_calls=[],
        destination="human_support",
        error={"code": "database_error", "message": "Unavailable"},
    )
    assert TriageResult.model_validate(result(**changes)).urgency is None
    with pytest.raises(ValidationError):
        TriageResult.model_validate(result(**changes, next_action="auto_respond"))
