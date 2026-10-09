"""Repository-independent database management entry point."""

import argparse
import json
import sys
from pathlib import Path

import psycopg
from pydantic import ValidationError

from triage_agent.knowledge.database import KnowledgeError, migrate
from triage_agent.knowledge.embeddings import configured_embedder
from triage_agent.knowledge.postgres_store import PostgresStore
from triage_agent.schemas import KnowledgeArticle, SearchArguments, Ticket
from triage_agent.tools import ToolDispatcher


def main(argv=None):
    parser = argparse.ArgumentParser(description="Classic RAG prototype management")
    parser.add_argument("command", choices=["migrate", "ingest", "stats", "search", "tool-demo"])
    parser.add_argument("--input", type=Path, default=Path("data/knowledge_base.json"))
    parser.add_argument("--tickets", type=Path, default=Path("data/sample_tickets.json"))
    parser.add_argument("--customers", type=Path, default=Path("data/customers.json"))
    parser.add_argument("--query")
    parser.add_argument("--locale", choices=["en", "th"])
    parser.add_argument("--product")
    parser.add_argument("--issue-type")
    args = parser.parse_args(argv)
    try:
        if args.command == "migrate":
            output = {"status": "ok", "vector_version": migrate()}
        else:
            embedder = configured_embedder()
            store = PostgresStore(embedder)
            if args.command == "ingest":
                articles = json.loads(args.input.read_text(encoding="utf-8"))
                output = store.ingest([KnowledgeArticle.model_validate(a) for a in articles])
            elif args.command == "stats":
                output = store.stats()
            elif args.command == "search":
                if not args.query:
                    parser.error("search requires --query")
                documents = store.search(
                    SearchArguments(
                        query=args.query,
                        product=args.product,
                        issue_type=args.issue_type,
                        locale=args.locale,
                    )
                )
                output = {"documents": [d.model_dump() for d in documents]}
            else:
                tickets = [
                    Ticket.model_validate(t)
                    for t in json.loads(args.tickets.read_text(encoding="utf-8"))
                ]
                tools = ToolDispatcher(args.customers, store)
                output = {"mode": "tools_only", "embedding_model": embedder.model, "tickets": []}
                for ticket in tickets:
                    history = tools.call(
                        "get_customer_history", {"customer_id": ticket.customer_id}
                    )
                    knowledge = tools.call(
                        "search_knowledge_base",
                        {
                            "query": "\n".join(m.text for m in ticket.messages),
                            "locale": ticket.locale,
                        },
                    )
                    output["tickets"].append(
                        {"ticket_id": ticket.ticket_id, "history": history, "knowledge": knowledge}
                    )
                if any(
                    t[tool]["status"] != "ok"
                    for t in output["tickets"]
                    for tool in ("history", "knowledge")
                ):
                    print(json.dumps(output, ensure_ascii=False))
                    return 2
        print(json.dumps(output, ensure_ascii=False))
        return 0
    except (psycopg.Error, KnowledgeError, OSError, ValueError, ValidationError):
        print(
            "Knowledge operation failed; check database, input or configuration.", file=sys.stderr
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
