"""Bounded, read-only tool loop with evidence validation and visible fallback."""

import json
from importlib.resources import files

from pydantic import ValidationError

from triage_agent.models import Model, ModelError
from triage_agent.policy import validate_decision
from triage_agent.schemas import ResultError, Ticket, ToolCall, TriageResult
from triage_agent.tools import TOOL_DEFINITIONS, ToolDispatcher


class Agent:
    def __init__(self, model: Model, tools: ToolDispatcher):
        self.model, self.tools = model, tools

    def triage(self, ticket: Ticket) -> TriageResult:
        prompt = files("triage_agent").joinpath("prompts/system.txt").read_text(encoding="utf-8")
        prompt += "\nTriageResult JSON schema:\n" + json.dumps(TriageResult.model_json_schema())
        messages = [
            dict(role="system", content=prompt),
            dict(role="user", content=ticket.model_dump_json()),
        ]
        calls, documents, used_ids = [], {}, set()
        correction_used = False
        executions = 0
        for _ in range(6):
            try:
                turn = self.model.complete(messages, TOOL_DEFINITIONS)
            except ModelError as exc:
                if exc.transient and not correction_used:
                    correction_used = True
                    continue
                return self._fallback(ticket, calls, "model_unavailable")
            if turn.calls:
                if executions + len(turn.calls) > 8:
                    return self._fallback(ticket, calls, "tool_budget_exhausted")
                # Validate the entire batch before executing any part of it.
                arguments = []
                try:
                    for call in turn.calls:
                        if not call.id or call.id in used_ids:
                            raise ValueError("duplicate_tool_id")
                        used_ids.add(call.id)
                        if call.name not in {"get_customer_history", "search_knowledge_base"}:
                            raise ValueError("unknown_tool")
                        args = json.loads(call.arguments)
                        if not isinstance(args, dict):
                            raise ValueError("invalid_tool_arguments")
                        if (
                            call.name == "get_customer_history"
                            and args.get("customer_id") != ticket.customer_id
                        ):
                            raise ValueError("wrong_customer")
                        arguments.append(args)
                except (ValueError, TypeError):
                    return self._fallback(ticket, calls, "invalid_tool_call")
                messages.append(
                    dict(
                        role="assistant",
                        content=turn.content,
                        tool_calls=[c.as_message() for c in turn.calls],
                    )
                )
                for call, args in zip(turn.calls, arguments, strict=True):
                    executions += 1
                    output = self.tools.call(call.name, args)
                    calls.append(ToolCall(name=call.name, call_id=call.id, status=output["status"]))
                    messages.append(
                        dict(
                            role="tool",
                            tool_call_id=call.id,
                            content=json.dumps(output, ensure_ascii=False),
                        )
                    )
                    if output["status"] == "error":
                        return self._fallback(ticket, calls, "tool_unavailable")
                    for document in output.get("documents", []):
                        documents[document["chunk_id"]] = document
                continue
            try:
                value = json.loads(turn.content or "")
                if not isinstance(value, dict):
                    raise ValueError("invalid_output")
                return validate_decision(value, ticket, calls, documents)
            except (ValueError, TypeError, ValidationError):
                if correction_used:
                    return self._fallback(ticket, calls, "invalid_model_output")
                correction_used = True
                messages.append(dict(role="assistant", content=turn.content or ""))
                messages.append(
                    dict(
                        role="user",
                        content="Application validation rejected the JSON. "
                        "Use the supplied schema, execute both tools, cite only actual "
                        "retrieved chunk IDs, and obey action policy. Correct once.",
                    )
                )
        return self._fallback(ticket, calls, "model_budget_exhausted")

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
