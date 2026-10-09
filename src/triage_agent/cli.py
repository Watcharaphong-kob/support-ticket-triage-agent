"""JSON terminal interface to the shared framework agent."""

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from triage_agent import __version__
from triage_agent.agent import triage_batch
from triage_agent.knowledge.database import KnowledgeError


def main(argv: Sequence[str] | None = None) -> int:
    # Preserve Thai JSON when Windows redirects stdout/stderr using a legacy encoding.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(
        prog="triage-agent", description="Support ticket triage prototype"
    )
    parser.add_argument("--input", type=Path, help="One ticket or a list of tickets in JSON")
    parser.add_argument("--customers", type=Path, default=Path("data/customers.json"))
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
        envelope = triage_batch(raw, customers_path=args.customers)
    except (OSError, ValueError, TypeError, KnowledgeError):
        print(
            "Input/configuration invalid; check JSON, paths and required environment settings.",
            file=sys.stderr,
        )
        return 2
    for result in envelope["results"]:
        if args.trace:
            print(
                json.dumps(
                    {
                        "ticket_id": result["ticket_id"],
                        "tool_calls": result["tool_calls"],
                        "status": result["status"],
                    },
                    ensure_ascii=False,
                ),
                file=sys.stderr,
            )
    print(
        json.dumps(
            envelope,
            ensure_ascii=False,
            indent=2,
        )
    )
    return 1 if any(r["status"] == "fallback" for r in envelope["results"]) else 0
