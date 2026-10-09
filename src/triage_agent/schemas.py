"""Public ticket, tool and decision contracts for the prototype."""

from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

NonEmpty = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
ToolName = Literal["get_customer_history", "search_knowledge_base"]


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class Message(Contract):
    sequence: int = Field(ge=1)
    relative_time: NonEmpty
    text: str = Field(min_length=1)
    supplied_translation: str | None


class Ticket(Contract):
    ticket_id: NonEmpty
    customer_id: NonEmpty
    is_synthetic_id: bool
    source_sample: int = Field(ge=1)
    locale: Literal["en", "th"]
    customer_info: NonEmpty
    messages: list[Message] = Field(min_length=1)

    @model_validator(mode="after")
    def ordered_messages(self) -> Self:
        if [m.sequence for m in self.messages] != list(range(1, len(self.messages) + 1)):
            raise ValueError("Messages must have consecutive sequence numbers starting at 1")
        return self


class Customer(Contract):
    customer_id: NonEmpty
    plan: Literal["Free", "Pro", "Enterprise"]
    tenure_months: int = Field(ge=0)
    region: NonEmpty | None
    seats: int | None = Field(ge=1)
    prior_support_summary: NonEmpty
    is_synthetic: bool
    source_sample: int = Field(ge=1)


class HistoryArguments(Contract):
    customer_id: NonEmpty


class SearchArguments(Contract):
    query: NonEmpty = Field(max_length=8000)
    product: NonEmpty | None = None
    issue_type: NonEmpty | None = None
    locale: Literal["en", "th"] | None = None


class KnowledgeArticle(Contract):
    id: NonEmpty
    title: NonEmpty
    content: NonEmpty
    locale: Literal["en", "th"]
    product: NonEmpty | None
    issue_type: NonEmpty
    version: NonEmpty
    is_mock: bool


class KnowledgeDocument(Contract):
    id: NonEmpty
    chunk_id: NonEmpty
    title: NonEmpty
    excerpt: NonEmpty
    locale: Literal["en", "th"]
    version: NonEmpty
    is_mock: bool
    score: float = Field(ge=-1.000001, le=1.000001)


class HistoryResult(Contract):
    status: Literal["ok", "not_found", "error"]
    customer: Customer | None
    error: NonEmpty | None

    @model_validator(mode="after")
    def consistent(self) -> Self:
        if (self.status == "ok") != (self.customer is not None):
            raise ValueError("Only successful history has a customer")
        if (self.status == "error") != (self.error is not None):
            raise ValueError("Only failed history has an error")
        return self


class SearchResult(Contract):
    status: Literal["ok", "error"]
    documents: list[KnowledgeDocument] = Field(max_length=5)
    error: NonEmpty | None

    @model_validator(mode="after")
    def consistent(self) -> Self:
        if (self.status == "error") != (self.error is not None):
            raise ValueError("Only failed search has an error")
        if self.status == "error" and self.documents:
            raise ValueError("Failed search cannot provide successful evidence")
        return self


class ToolCall(Contract):
    name: ToolName
    call_id: NonEmpty
    status: Literal["ok", "not_found", "error"]


class ResultError(Contract):
    code: NonEmpty
    message: NonEmpty


class TriageResult(Contract):
    ticket_id: NonEmpty
    status: Literal["completed", "fallback"]
    urgency: Literal["critical", "high", "medium", "low"] | None
    product: NonEmpty | None
    issue_type: NonEmpty | None
    customer_sentiment: Literal["positive", "neutral", "frustrated", "angry", "mixed", "unknown"]
    secondary_issues: list[NonEmpty]
    next_action: Literal["auto_respond", "route_to_specialist", "escalate_to_human"]
    destination: (
        Literal[
            "incident_on_call",
            "billing_payments",
            "human_support",
            "product_support",
            "technical_support",
        ]
        | None
    )
    rationale: NonEmpty
    draft_response: NonEmpty | None
    knowledge_sources: list[NonEmpty]
    uncertainties: list[NonEmpty]
    tool_calls: list[ToolCall]
    error: ResultError | None

    @model_validator(mode="after")
    def consistent_decision(self) -> Self:
        if len({c.call_id for c in self.tool_calls}) != len(self.tool_calls):
            raise ValueError("Tool call IDs must be unique")
        if self.status == "fallback":
            if self.error is None or self.next_action != "escalate_to_human":
                raise ValueError("Fallback must record an error and escalate")
            if self.destination != "human_support":
                raise ValueError("Fallback destination must be human_support")
        else:
            if self.error is not None or self.urgency is None or self.issue_type is None:
                raise ValueError("Completed result requires urgency/issue and no error")
            succeeded = {c.name for c in self.tool_calls if c.status == "ok"}
            if succeeded != {"get_customer_history", "search_knowledge_base"}:
                raise ValueError("Both tools must succeed before completed triage")
        allowed = {
            "auto_respond": {None},
            "route_to_specialist": {"product_support", "technical_support"},
            "escalate_to_human": {"incident_on_call", "billing_payments", "human_support"},
        }
        if self.destination not in allowed[self.next_action]:
            raise ValueError("Action and destination conflict")
        if self.urgency == "critical" and self.next_action != "escalate_to_human":
            raise ValueError("Critical results must escalate")
        if self.next_action == "auto_respond" and not self.knowledge_sources:
            raise ValueError("Auto-response requires knowledge evidence")
        return self
