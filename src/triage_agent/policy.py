"""Validate decisions against actual execution evidence, never provider claims."""

from triage_agent.schemas import Ticket, ToolCall, TriageResult


def validate_decision(
    value: dict, ticket: Ticket, calls: list[ToolCall], documents: dict
) -> TriageResult:
    if value.get("ticket_id") != ticket.ticket_id or value.get("status") != "completed":
        raise ValueError("invalid_identity_or_status")
    if value.get("tool_calls"):
        raise ValueError("fabricated_tool_records")
    value = dict(value, tool_calls=[c.model_dump() for c in calls])
    result = TriageResult.model_validate(value)
    if any(c.status == "error" for c in calls):
        raise ValueError("tool_failure")
    if any(source not in documents for source in result.knowledge_sources):
        raise ValueError("invalid_citation")
    if (
        result.urgency != "critical"
        and result.issue_type == "billing"
        and (result.next_action != "escalate_to_human" or result.destination != "billing_payments")
    ):
        raise ValueError("billing_requires_human")
    if result.urgency == "critical" and result.destination != "incident_on_call":
        raise ValueError("critical_requires_incident")
    if result.next_action == "auto_respond" and (
        result.urgency != "low"
        or not result.draft_response
        or any(c.status == "not_found" for c in calls)
    ):
        raise ValueError("unsafe_auto_response")
    if (
        ticket.locale == "th"
        and result.draft_response
        and not any("\u0e00" <= char <= "\u0e7f" for char in result.draft_response)
    ):
        raise ValueError("thai_draft_required")
    if any(c.status == "not_found" for c in calls):
        result.uncertainties.append("Customer history not found; decision uses conversation only.")
    if any(documents[s]["is_mock"] for s in result.knowledge_sources):
        result.uncertainties.append(
            "Cited knowledge is synthetic demonstration material, not verified company policy."
        )
        if result.next_action == "auto_respond":
            prefix = (
                "ร่างสาธิตจากเอกสารตัวอย่าง: "
                if ticket.locale == "th"
                else "Demonstration draft using mock knowledge: "
            )
            result.draft_response = prefix + result.draft_response
    return result
