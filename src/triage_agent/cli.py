"""CLI startup; ticket processing is implemented in subsequent tasks."""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from triage_agent import __version__


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="triage-agent",
        description="Support ticket triage agent (T02 setup; processing not implemented yet).",
    )
    parser.add_argument(
        "--input", type=Path, help="JSON ticket file (available after agent integration)"
    )
    parser.add_argument("--trace", action="store_true", help="Show tool traces on stderr")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)
    if args.input is None:
        parser.print_help()
        return 0
    print(
        "Ticket processing is not implemented yet; this release completes T02 setup.",
        file=sys.stderr,
    )
    return 2
