"""Two read-only, allowlisted tools; errors never masquerade as retrieved evidence."""

import json
from pathlib import Path

from langchain_core.tools import StructuredTool
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

TOOL_SCHEMAS = {
    "get_customer_history": HistoryArguments,
    "search_knowledge_base": SearchArguments,
}

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

    def framework_tools(self) -> list[StructuredTool]:
        tools = []
        for definition in TOOL_DEFINITIONS:
            function = definition["function"]
            name = function["name"]

            def invoke(tool_name=name, **arguments):
                return self.call(tool_name, arguments)

            tools.append(
                StructuredTool.from_function(
                    func=invoke,
                    name=name,
                    description=function["description"],
                    args_schema=TOOL_SCHEMAS[name],
                )
            )
        return tools

    def call(self, name: str, arguments: dict) -> dict:
        if name not in TOOL_SCHEMAS:
            return {"status": "error", "error": "unknown_tool"}
        try:
            args = TOOL_SCHEMAS[name].model_validate(arguments)
            if name == "get_customer_history":
                return self.get_customer_history(args.customer_id).model_dump()
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
