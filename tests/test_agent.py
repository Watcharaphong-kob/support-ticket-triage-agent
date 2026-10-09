import json
from pathlib import Path

import httpx
import pytest
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import Field

from triage_agent.agent import Agent
from triage_agent.schemas import Ticket
from triage_agent.tools import ToolDispatcher

ROOT = Path(__file__).resolve().parents[1]


class ScriptedChatModel(BaseChatModel):
    """Replace only the paid model; execute the real framework and tools."""

    turns: list = Field(default_factory=list)
    observed: list = Field(default_factory=list)

    @property
    def _llm_type(self):
        return "scripted-test-chat"

    def bind_tools(self, tools, **kwargs):
        return self

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        self.observed.append(list(messages))
        turn = self.turns[len(self.observed) - 1]
        if isinstance(turn, Exception):
            raise turn
        return ChatResult(generations=[ChatGeneration(message=turn)])


class EmptyKnowledge:
    def search(self, arguments):
        return []


def ticket(index=0):
    return Ticket.model_validate(
        json.loads((ROOT / "data/sample_tickets.json").read_text(encoding="utf-8"))[index]
    )


def tool_requests(customer="customer-001"):
    return AIMessage(
        content="",
        tool_calls=[
            {"id": "h", "name": "get_customer_history", "args": {"customer_id": customer}},
            {"id": "k", "name": "search_knowledge_base", "args": {"query": "payment charges"}},
        ],
    )


def decision(**changes):
    value = dict(
        ticket_id="ticket-001",
        status="completed",
        urgency="high",
        product=None,
        issue_type="billing",
        customer_sentiment="angry",
        secondary_issues=["missing Pro access"],
        next_action="escalate_to_human",
        destination="billing_payments",
        rationale="Repeated reported charges and urgent presentation; settlement unverified.",
        draft_response=None,
        knowledge_sources=[],
        uncertainties=["Settlement unknown"],
        tool_calls=[],
        error=None,
    )
    value.update(changes)
    return AIMessage(
        content="",
        tool_calls=[
            {"id": "decision", "name": "TriageResult", "args": value},
        ],
    )


def test_framework_terminal_seam_preserves_thread_and_real_tool_evidence():
    model = ScriptedChatModel(turns=[tool_requests(), decision()])
    result = Agent(model, ToolDispatcher(ROOT / "data/customers.json", EmptyKnowledge())).triage(
        ticket()
    )
    assert result.status == "completed"
    assert result.destination == "billing_payments"
    assert [(c.name, c.call_id) for c in result.tool_calls] == [
        ("get_customer_history", "h"),
        ("search_knowledge_base", "k"),
    ]
    assert json.loads(model.observed[0][1].content) == ticket().model_dump()
    assert {m.tool_call_id for m in model.observed[-1] if m.type == "tool"} == {"h", "k"}


def test_unauthorized_batch_rejects_valid_prefix_before_any_tool_execution():
    class MustNotSearch:
        def search(self, arguments):
            raise AssertionError("Rejected batch must execute no tools")

    request = tool_requests("foreign-customer")
    request.tool_calls.reverse()
    result = Agent(
        ScriptedChatModel(turns=[request]),
        ToolDispatcher(ROOT / "data/customers.json", MustNotSearch()),
    ).triage(ticket())
    assert result.status == "fallback"
    assert result.error.code == "invalid_tool_call"
    assert result.tool_calls == []


@pytest.mark.parametrize(
    "turns,code",
    [
        ([RuntimeError("private-provider-detail")], "model_unavailable"),
        ([decision()], "invalid_model_output"),
        ([tool_requests(), decision(knowledge_sources=["forged"])], "invalid_model_output"),
    ],
)
def test_unverifiable_runs_return_safe_fallback_without_retry(turns, code):
    model = ScriptedChatModel(turns=turns)
    result = Agent(model, ToolDispatcher(ROOT / "data/customers.json", EmptyKnowledge())).triage(
        ticket()
    )
    assert result.status == "fallback"
    assert result.error.code == code
    assert result.destination == "human_support"
    assert len(model.observed) == len(turns)
    assert "private" not in result.model_dump_json()


@pytest.mark.parametrize(
    "count,code,executed",
    [
        (9, "tool_budget_exhausted", 0),
        (1, "model_budget_exhausted", 6),
    ],
)
def test_run_budgets_stop_before_extra_calls(count, code, executed):
    turns = [
        AIMessage(
            content="",
            tool_calls=[
                {"id": f"{step}-{i}", "name": "search_knowledge_base", "args": {"query": "theme"}}
                for i in range(count)
            ],
        )
        for step in range(7)
    ]
    model = ScriptedChatModel(turns=turns)
    result = Agent(model, ToolDispatcher(ROOT / "data/customers.json", EmptyKnowledge())).triage(
        ticket()
    )
    assert result.error.code == code
    assert len(result.tool_calls) == executed
    assert len(model.observed) <= 6


def test_critical_billing_escalates_to_incident_review():
    result = Agent(
        ScriptedChatModel(
            turns=[tool_requests(), decision(urgency="critical", destination="incident_on_call")]
        ),
        ToolDispatcher(ROOT / "data/customers.json", EmptyKnowledge()),
    ).triage(ticket())
    assert result.status == "completed"
    assert result.destination == "incident_on_call"


@pytest.mark.parametrize("status", [401, 429, 500])
def test_configured_provider_failure_is_sanitized_and_not_retried(status):
    from triage_agent.config import Settings

    received = []

    def unavailable(request):
        received.append(json.loads(request.content))
        return httpx.Response(status, json={"error": {"message": "private-provider-detail"}})

    model = Settings("test-key", "configured-gpt").chat_model(
        http_client=httpx.Client(transport=httpx.MockTransport(unavailable))
    )
    result = Agent(model, ToolDispatcher(ROOT / "data/customers.json", EmptyKnowledge())).triage(
        ticket()
    )
    assert result.error.code == "model_unavailable"
    assert len(received) == 1
    assert received[0]["model"] == "configured-gpt"
    assert received[0]["store"] is False
    assert "private" not in result.model_dump_json()


def test_truncated_provider_decision_cannot_complete():
    final = decision()
    final.response_metadata = {"finish_reason": "length"}
    result = Agent(
        ScriptedChatModel(turns=[tool_requests(), final]),
        ToolDispatcher(ROOT / "data/customers.json", EmptyKnowledge()),
    ).triage(ticket())
    assert result.status == "fallback"
    assert result.error.code == "invalid_model_output"


@pytest.mark.parametrize(
    "tool_request",
    [
        AIMessage(content="", tool_calls=[{"id": "bad", "name": "delete_account", "args": {}}]),
        AIMessage(
            content="",
            tool_calls=[
                {
                    "id": "bad",
                    "name": "search_knowledge_base",
                    "args": {"query": "x", "sql": "DROP"},
                }
            ],
        ),
        AIMessage(
            content="",
            invalid_tool_calls=[
                {
                    "id": "bad",
                    "name": "search_knowledge_base",
                    "args": "[]",
                    "error": "invalid JSON",
                }
            ],
        ),
    ],
)
def test_invalid_calls_cannot_execute(tool_request):
    result = Agent(
        ScriptedChatModel(turns=[tool_request]),
        ToolDispatcher(ROOT / "data/customers.json", EmptyKnowledge()),
    ).triage(ticket())
    assert result.error.code == "invalid_tool_call"
    assert result.tool_calls == []


def test_duplicate_tool_ids_fail_after_preserving_prior_evidence():
    result = Agent(
        ScriptedChatModel(turns=[tool_requests(), tool_requests()]),
        ToolDispatcher(ROOT / "data/customers.json", EmptyKnowledge()),
    ).triage(ticket())
    assert result.error.code == "invalid_tool_call"
    assert len(result.tool_calls) == 2


def test_missing_history_is_disclosed_without_fabrication():
    current = ticket().model_copy(update={"customer_id": "missing"})
    result = Agent(
        ScriptedChatModel(turns=[tool_requests("missing"), decision()]),
        ToolDispatcher(ROOT / "data/customers.json", EmptyKnowledge()),
    ).triage(current)
    assert result.status == "completed"
    assert result.tool_calls[0].status == "not_found"
    assert any("history not found" in u for u in result.uncertainties)


def test_tool_failure_retains_actual_failed_execution_and_safe_error():
    from triage_agent.knowledge.database import KnowledgeError

    class BrokenKnowledge:
        def search(self, arguments):
            raise KnowledgeError("private connection details")

    result = Agent(
        ScriptedChatModel(turns=[tool_requests()]),
        ToolDispatcher(ROOT / "data/customers.json", BrokenKnowledge()),
    ).triage(ticket())
    assert result.error.code == "tool_unavailable"
    assert any(c.status == "error" and c.name == "search_knowledge_base" for c in result.tool_calls)
    assert "private" not in result.model_dump_json()


def test_thai_ticket_rejects_english_only_draft():
    current = ticket(1)
    result = Agent(
        ScriptedChatModel(
            turns=[
                tool_requests(current.customer_id),
                decision(ticket_id=current.ticket_id, draft_response="English only"),
            ]
        ),
        ToolDispatcher(ROOT / "data/customers.json", EmptyKnowledge()),
    ).triage(current)
    assert result.error.code == "invalid_model_output"


def test_eight_real_tools_plus_structured_helper_can_complete():
    request = tool_requests()
    request = AIMessage(
        content="",
        tool_calls=request.tool_calls
        + [
            {"id": f"extra-{i}", "name": "search_knowledge_base", "args": {"query": "theme"}}
            for i in range(6)
        ],
    )
    result = Agent(
        ScriptedChatModel(turns=[request, decision()]),
        ToolDispatcher(ROOT / "data/customers.json", EmptyKnowledge()),
    ).triage(ticket())
    assert result.status == "completed"
    assert len(result.tool_calls) == 8
