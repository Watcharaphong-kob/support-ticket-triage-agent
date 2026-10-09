"""Provider seam; live GPT and explicitly labeled deterministic demonstrations."""

import json
from dataclasses import dataclass, field
from typing import Protocol

from openai import APIConnectionError, APIStatusError, OpenAI, OpenAIError


@dataclass(frozen=True)
class ModelCall:
    id: str
    name: str
    arguments: str

    def as_message(self) -> dict:
        return {
            "id": self.id,
            "type": "function",
            "function": {"name": self.name, "arguments": self.arguments},
        }


@dataclass(frozen=True)
class ModelTurn:
    content: str | None = None
    calls: list[ModelCall] = field(default_factory=list)


class ModelError(Exception):
    def __init__(self, transient: bool = False):
        self.transient = transient
        super().__init__("Model request failed")


class Model(Protocol):
    def complete(self, messages: list[dict], tools: list[dict]) -> ModelTurn: ...


class OpenAIModel:
    def __init__(self, api_key: str, model: str, *, client=None):
        self.model = model
        self.client = client or OpenAI(api_key=api_key, timeout=30.0, max_retries=0)

    def complete(self, messages: list[dict], tools: list[dict]) -> ModelTurn:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                response_format={"type": "json_object"},
                max_completion_tokens=4096,
                timeout=30.0,
                store=False,
            )
            if not response.choices:
                raise ModelError()
            choice = response.choices[0]
            message = choice.message
            if message.refusal or choice.finish_reason in {"length", "content_filter"}:
                raise ModelError()
            calls = []
            for call in message.tool_calls or []:
                if call.type != "function":
                    raise ModelError()
                calls.append(ModelCall(call.id, call.function.name, call.function.arguments))
            return ModelTurn(content=message.content, calls=calls)
        except APIConnectionError:
            raise ModelError(transient=True) from None
        except APIStatusError as exc:
            raise ModelError(transient=exc.status_code == 429 or exc.status_code >= 500) from None
        except OpenAIError:
            raise ModelError() from None


class OfflineModel:
    """Simple scenario rules for plumbing tests, NOT GPT or a quality benchmark."""

    def complete(self, messages: list[dict], tools: list[dict]) -> ModelTurn:
        ticket = json.loads(messages[1]["content"])
        text = "\n".join(
            m["text"] + "\n" + (m["supplied_translation"] or "") for m in ticket["messages"]
        )
        lowered = text.lower()
        if "charge" in lowered or "payment" in lowered:
            issue, urgency, destination, sentiment = "billing", "high", "billing_payments", "angry"
            query = "payment failed upgrade Pro repeated charges missing access"
            rationale = (
                "Reported repeated $29.99 charges, missing Pro access and a presentation "
                "in two hours; settlement and refund outcomes remain unverified."
            )
            secondary = ["missing Pro access"]
            uncertainty = ["Reported charges may be pending; settlement and reversal not verified."]
            draft = (
                "Demonstration draft: Your reported charges and missing access need urgent "
                "billing review. No refund outcome or deadline is confirmed."
            )
        elif "500" in lowered:
            issue, urgency, destination, sentiment = (
                "service_access",
                "critical",
                "incident_on_call",
                "frustrated",
            )
            query = "ระบบเข้าไม่ได้ error 500 หลายเครื่อง เพื่อนร่วมงาน demo region Asia"
            rationale = (
                "Reported error 500 across devices, browsers and coworkers, with an "
                "imminent major-client demo. A green status page does not resolve the report."
            )
            secondary = ["business demo blocked"]
            uncertainty = ["Regional outage and affected seat count have not been verified."]
            draft = (
                "ร่างสาธิต: รับทราบปัญหา error 500 ที่กระทบหลายเครื่องและเพื่อนร่วมงาน "
                "ควรส่งให้ทีม incident ตรวจสอบเร่งด่วน ยังไม่ยืนยันปัญหา region Asia หรือเวลาซ่อม"
            )
        elif "dark" in lowered or "theme" in lowered:
            issue, urgency, destination, sentiment = "theme", "low", "product_support", "mixed"
            query = "System Default macOS dark mode stays light theme scheduling feature request"
            rationale = (
                "Nonblocking theme behavior persists after trying System Default; "
                "preserve the separate scheduling request instead of repeating failed advice."
            )
            secondary = ["scheduled dark mode feature request"]
            uncertainty = ["Theme bug and availability of dark mode/scheduling are unverified."]
            draft = (
                "Demonstration draft: The failed System Default behavior needs product "
                "investigation. We will keep scheduling as a separate feature request; "
                "availability is not confirmed."
            )
        else:
            issue, urgency, destination, sentiment = "general", "medium", "human_support", "unknown"
            query = text[:8000]
            rationale = (
                "Offline demonstration cannot classify this scenario reliably; "
                "request human review."
            )
            secondary, uncertainty, draft = [], ["Offline scenario rules are limited."], None
        outputs = [json.loads(m["content"]) for m in messages if m["role"] == "tool"]
        if not outputs:
            return ModelTurn(
                calls=[
                    ModelCall(
                        "history",
                        "get_customer_history",
                        json.dumps({"customer_id": ticket["customer_id"]}),
                    ),
                    ModelCall(
                        "knowledge",
                        "search_knowledge_base",
                        json.dumps({"query": query}, ensure_ascii=False),
                    ),
                ]
            )
        sources = [d["chunk_id"] for output in outputs for d in output.get("documents", [])]
        return ModelTurn(
            content=json.dumps(
                dict(
                    ticket_id=ticket["ticket_id"],
                    status="completed",
                    urgency=urgency,
                    product=None,
                    issue_type=issue,
                    customer_sentiment=sentiment,
                    secondary_issues=secondary,
                    next_action="route_to_specialist"
                    if destination == "product_support"
                    else "escalate_to_human",
                    destination=destination,
                    rationale=rationale,
                    draft_response=draft,
                    knowledge_sources=sources,
                    uncertainties=uncertainty,
                    tool_calls=[],
                    error=None,
                ),
                ensure_ascii=False,
            )
        )
