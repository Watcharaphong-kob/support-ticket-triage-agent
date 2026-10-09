"""JSON batch CLI: live GPT by default; explicit offline demonstrations."""

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from triage_agent import __version__
from triage_agent.agent import Agent
from triage_agent.config import Settings
from triage_agent.knowledge.database import KnowledgeError
from triage_agent.knowledge.embeddings import configured_embedder
from triage_agent.knowledge.postgres_store import PostgresStore
from triage_agent.models import OfflineModel, OpenAIModel
from triage_agent.schemas import Ticket
from triage_agent.tools import ToolDispatcher


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="triage-agent", description="Support ticket triage prototype"
    )
    parser.add_argument("--input", type=Path, help="One ticket or a list of tickets in JSON")
    parser.add_argument("--customers", type=Path, default=Path("data/customers.json"))
    parser.add_argument(
        "--offline", action="store_true", help="Use labeled deterministic demonstration model"
    )
    parser.add_argument(
        "--trace", action="store_true", help="Show safe tool status traces on stderr"
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)
    if args.input is None:
        parser.print_help()
        return 0
    try:
        raw = json.loads(args.input.read_text(encoding="utf-8"))
        records = raw if isinstance(raw, list) else [raw]
        if not records or len(records) > 100:
            raise ValueError("Batch must contain 1–100 tickets")
        tickets = [Ticket.model_validate(t) for t in records]
        if len({t.ticket_id for t in tickets}) != len(tickets):
            raise ValueError("Duplicate ticket IDs")
        model = (
            OfflineModel()
            if args.offline
            else OpenAIModel(*Settings.from_env().require_live_credentials())
        )
        embedder = configured_embedder()
        tools = ToolDispatcher(args.customers, PostgresStore(embedder))
    except (OSError, ValueError, TypeError, KnowledgeError):
        print(
            "Input/configuration invalid; check JSON, paths and required environment settings.",
            file=sys.stderr,
        )
        return 2
    agent = Agent(model, tools)
    results = []
    for ticket in tickets:
        result = agent.triage(ticket)
        results.append(result.model_dump())
        if args.trace:
            print(
                json.dumps(
                    {
                        "ticket_id": ticket.ticket_id,
                        "tool_calls": [c.model_dump() for c in result.tool_calls],
                        "status": result.status,
                    },
                    ensure_ascii=False,
                ),
                file=sys.stderr,
            )
    print(
        json.dumps(
            {
                "mode": "offline_demo" if args.offline else "live_gpt",
                "embedding_model": embedder.model,
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 1 if any(r["status"] == "fallback" for r in results) else 0
