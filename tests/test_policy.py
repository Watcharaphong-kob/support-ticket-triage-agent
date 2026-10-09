import pytest
from test_agent import decision, ticket

from triage_agent.policy import validate_decision
from triage_agent.schemas import ToolCall

CALLS = [
    ToolCall(name="get_customer_history", call_id="h", status="ok"),
    ToolCall(name="search_knowledge_base", call_id="k", status="ok"),
]


def validate(**changes):
    return validate_decision(
        decision(**changes).tool_calls[0]["args"],
        ticket(),
        CALLS,
        {"real-chunk": {"is_mock": False}, "mock-chunk": {"is_mock": True}},
    )


def test_unknown_citation_is_rejected():
    with pytest.raises(ValueError):
        validate(knowledge_sources=["invented"])


def test_billing_cannot_auto_respond_or_route_to_specialist():
    with pytest.raises(ValueError):
        validate(next_action="route_to_specialist", destination="product_support")


def test_mock_faq_auto_response_is_labeled_demonstration_draft():
    result = validate(
        issue_type="faq",
        urgency="low",
        next_action="auto_respond",
        destination=None,
        draft_response="Here is the answer.",
        knowledge_sources=["mock-chunk"],
    )
    assert result.draft_response.startswith("Demonstration draft using mock knowledge:")
    assert any("synthetic" in u for u in result.uncertainties)


def test_auto_response_without_draft_is_rejected():
    with pytest.raises(ValueError):
        validate(
            issue_type="faq",
            urgency="low",
            next_action="auto_respond",
            destination=None,
            draft_response=None,
            knowledge_sources=["real-chunk"],
        )


def test_high_urgency_cannot_auto_respond_even_with_valid_faq_evidence():
    with pytest.raises(ValueError):
        validate(
            issue_type="faq",
            urgency="high",
            next_action="auto_respond",
            destination=None,
            draft_response="Answer",
            knowledge_sources=["real-chunk"],
        )
