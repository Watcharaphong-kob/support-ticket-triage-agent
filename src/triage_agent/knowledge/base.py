"""Knowledge-tool boundary, independent of its storage backend."""

from typing import Protocol

from triage_agent.schemas import KnowledgeDocument, SearchArguments


class KnowledgeStore(Protocol):
    def search(self, arguments: SearchArguments) -> list[KnowledgeDocument]: ...
