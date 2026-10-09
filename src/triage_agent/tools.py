"""Two read-only, allowlisted tools; errors never masquerade as retrieved evidence."""

import json
from pathlib import Path

from pydantic import ValidationError

from triage_agent.knowledge.base import KnowledgeStore
from triage_agent.knowledge.database import KnowledgeError
from triage_agent.schemas import (
    Customer,
    HistoryArguments,
    HistoryResult,
    SearchArguments,
    SearchResult,
)

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_customer_history",
            "description": "Read synthetic customer context; not a live billing/account record.",
            "parameters": HistoryArguments.model_json_schema(),
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "Retrieve up to five cited passages from PostgreSQL classic RAG. "
            "Mock evidence is illustrative and cannot verify real policy or incidents.",
            "parameters": SearchArguments.model_json_schema(),
        },
    },
]


class ToolDispatcher:
    def __init__(self, customers_path: Path, knowledge: KnowledgeStore):
        self.customers_path, self.knowledge = customers_path, knowledge

    def call(self, name: str, arguments: dict) -> dict:
        if name not in {"get_customer_history", "search_knowledge_base"}:
            return {"status": "error", "error": "unknown_tool"}
        try:
            if name == "get_customer_history":
                args = HistoryArguments.model_validate(arguments)
                return self.get_customer_history(args.customer_id).model_dump()
            args = SearchArguments.model_validate(arguments)
            return self.search_knowledge_base(args).model_dump()
        except ValidationError:
            if name == "get_customer_history":
                return HistoryResult(
                    status="error", customer=None, error="invalid_tool_arguments"
                ).model_dump()
            return SearchResult(
                status="error", documents=[], error="invalid_tool_arguments"
            ).model_dump()

    def get_customer_history(self, customer_id: str) -> HistoryResult:
        try:
            records = json.loads(self.customers_path.read_text(encoding="utf-8"))
            customers = [Customer.model_validate(record) for record in records]
            if len({c.customer_id for c in customers}) != len(customers):
                raise ValueError("Duplicate customer identifiers")
            found = next((c for c in customers if c.customer_id == customer_id), None)
            return HistoryResult(status="ok" if found else "not_found", customer=found, error=None)
        except (OSError, ValueError, TypeError):
            return HistoryResult(
                status="error", customer=None, error="customer_history_unavailable"
            )

    def search_knowledge_base(self, arguments: SearchArguments) -> SearchResult:
        try:
            documents = self.knowledge.search(arguments)
            return SearchResult(status="ok", documents=documents, error=None)
        except KnowledgeError:
            return SearchResult(status="error", documents=[], error="knowledge_unavailable")
