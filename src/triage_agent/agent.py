"""One LangChain agent on LangGraph; application-owned evidence validation."""

import json
from importlib.resources import files
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import (
    ModelCallLimitMiddleware,
    ToolCallLimitMiddleware,
    after_model,
    wrap_model_call,
    wrap_tool_call,
)
from langchain.agents.middleware.model_call_limit import ModelCallLimitExceededError
from langchain.agents.middleware.tool_call_limit import ToolCallLimitExceededError
from langchain.agents.structured_output import StructuredOutputError, ToolStrategy
from langchain_core.language_models import BaseChatModel
from langgraph.errors import GraphRecursionError

from triage_agent.config import Settings
from triage_agent.knowledge.embeddings import configured_embedder
from triage_agent.knowledge.postgres_store import PostgresStore
from triage_agent.policy import validate_decision
from triage_agent.schemas import (
    ResultError,
    Ticket,
    ToolCall,
    TriageResult,
    validate_batch,
)
from triage_agent.tools import TOOL_SCHEMAS, ToolDispatcher


class TriageFailure(Exception):
    """Safe application failure code; never contains customer/provider details."""


class Agent:
    def __init__(self, model: BaseChatModel, tools: ToolDispatcher):
        self.model, self.tools = model, tools

    def triage(self, ticket: Ticket) -> TriageResult:
        prompt = files("triage_agent").joinpath("prompts/system.txt").read_text(encoding="utf-8")
        tools = self.tools.framework_tools()
        used_ids = set()
        call_order, records, documents = [], {}, {}

        @wrap_model_call
        def safe_model(request, handler):
            try:
                return handler(request)
            except StructuredOutputError:
                raise TriageFailure("invalid_model_output") from None
            except Exception:
                raise TriageFailure("model_unavailable") from None

        @wrap_tool_call
        def record_execution(request, handler):
            call = request.tool_call
            try:
                result = handler(request)
                output = json.loads(result.content)
            except Exception:
                output = {"status": "error"}
                result = None
            records[call["id"]] = ToolCall(
                name=call["name"],
                call_id=call["id"],
                status=output["status"],
            )
            if output["status"] == "error":
                raise TriageFailure("tool_unavailable")
            documents.update({d["chunk_id"]: d for d in output.get("documents", [])})
            return result

        @after_model
        def authorize_batch(state, runtime):
            message = next(m for m in reversed(state["messages"]) if m.type == "ai")
            if message.response_metadata.get("finish_reason") in {
                "length",
                "content_filter",
            } or message.additional_kwargs.get("refusal"):
                raise TriageFailure("invalid_model_output")
            if message.invalid_tool_calls:
                raise TriageFailure("invalid_tool_call")
            real_calls = [c for c in message.tool_calls if c["name"] != "TriageResult"]
            if len(call_order) + len(real_calls) > 8:
                raise TriageFailure("tool_budget_exhausted")
            if real_calls and len(real_calls) != len(message.tool_calls):
                raise TriageFailure("invalid_tool_call")
            for call in message.tool_calls:
                if not call["id"] or call["id"] in used_ids:
                    raise TriageFailure("invalid_tool_call")
                used_ids.add(call["id"])
                if call["name"] == "TriageResult":
                    continue
                if call["name"] not in TOOL_SCHEMAS:
                    raise TriageFailure("invalid_tool_call")
                try:
                    TOOL_SCHEMAS[call["name"]].model_validate(call["args"])
                except ValueError:
                    raise TriageFailure("invalid_tool_call") from None
                if (
                    call["name"] == "get_customer_history"
                    and call["args"]["customer_id"] != ticket.customer_id
                ):
                    raise TriageFailure("invalid_tool_call")
            call_order.extend(c["id"] for c in real_calls)

        graph = create_agent(
            self.model,
            tools,
            system_prompt=prompt,
            response_format=ToolStrategy(TriageResult.model_json_schema(), handle_errors=False),
            # The all-call guard includes the one structured-output helper; actual tools cap at 8.
            middleware=[
                ModelCallLimitMiddleware(run_limit=6, exit_behavior="error"),
                ToolCallLimitMiddleware(run_limit=9, exit_behavior="error"),
                safe_model,
                authorize_batch,
                record_execution,
            ],
        )
        try:
            state = graph.invoke(
                {"messages": [{"role": "user", "content": ticket.model_dump_json()}]},
                {"recursion_limit": 40},
            )
        except TriageFailure as exc:
            code = str(exc)
        except ModelCallLimitExceededError:
            code = "model_budget_exhausted"
        except ToolCallLimitExceededError:
            code = "tool_budget_exhausted"
        except GraphRecursionError:
            code = "graph_budget_exhausted"
        else:
            code = None
        calls = [records[c] for c in call_order if c in records]
        if code:
            return self._fallback(ticket, calls, code)
        try:
            return validate_decision(state["structured_response"], ticket, calls, documents)
        except (ValueError, TypeError, KeyError):
            return self._fallback(ticket, calls, "invalid_model_output")

    @staticmethod
    def _fallback(ticket: Ticket, calls: list[ToolCall], code: str) -> TriageResult:
        return TriageResult(
            ticket_id=ticket.ticket_id,
            status="fallback",
            urgency=None,
            product=None,
            issue_type=None,
            customer_sentiment="unknown",
            secondary_issues=[],
            next_action="escalate_to_human",
            destination="human_support",
            rationale="Automated triage could not be verified; human review is required.",
            draft_response=None,
            knowledge_sources=[],
            uncertainties=["Classification unavailable."],
            tool_calls=calls,
            error=ResultError(code=code, message="Triage could not be completed safely."),
        )


def triage_batch(value, *, customers_path=Path("data/customers.json"), model=None, knowledge=None):
    """Validate before constructing paid dependencies; share one result envelope."""
    tickets = validate_batch(value)
    if model is None:
        model = Settings.from_env().chat_model()
    if knowledge is None:
        knowledge = PostgresStore(configured_embedder())
    agent = Agent(model, ToolDispatcher(customers_path, knowledge))
    return {
        "mode": "live_gpt",
        "embedding_model": knowledge.embedder.model,
        "results": [agent.triage(t).model_dump() for t in tickets],
    }
