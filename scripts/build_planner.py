"""Build a small offline reader from the current plan and faithful assignment source."""

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/Watcharaphong-kob/support-ticket-triage-agent"


def main():
    source = json.loads((ROOT / "docs/assignment_source.json").read_text(encoding="utf-8"))
    plan = (ROOT / "plan.md").read_text(encoding="utf-8")
    paragraphs = "".join(
        f'<div data-source-paragraph="{p["index"]}">{escape(p["text"])}</div>'
        for p in source["paragraphs"]
    )
    page = f"""<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>Main Assignment — Framework Prototype</title>
<style>
body{{margin:0;background:#f5f6f8;color:#182431;font:17px/1.65 system-ui,sans-serif}}
main{{max-width:1000px;margin:auto;padding:28px}}nav{{position:sticky;top:0;background:#fff;padding:12px}}
a{{color:#135fc4}}nav
a{{margin-right:18px}}section{{scroll-margin-top:65px;background:#fff;padding:24px;margin:20px
0;border-radius:12px}}
h1,h2{{line-height:1.25}}.flow{{background:#e9f2ff;padding:18px;border-radius:8px}}
pre{{white-space:pre-wrap;overflow-wrap:anywhere;font:15px/1.65 ui-monospace,monospace}}
[data-source-paragraph]{{white-space:pre-wrap;padding:14px 0;border-bottom:1px solid #e0e5eb}}
</style><nav><a href="#summary">Summary</a><a href="#spec">Spec / TODO</a><a href="#stack">Tech
stack</a><a href="#original">Main Word</a></nav>
<main><h1>Support Ticket Triage Agent</h1>
<section id="summary"><h2>Framework prototype</h2><p>Main Word requirements govern behavior. Owner
scope adds uv, Docker classic RAG, LangChain/LangGraph, terminal and API. GraphRAG is next
phase.</p>
<div class="flow">CLI / FastAPI → shared batch validation → one LangChain agent on LangGraph →
customer history + PostgreSQL RAG → evidence/policy check → result or human fallback</div>
<p>Two real read-only tools; output helper does not count. Drafts are never sent. Scripted
tests/fake vectors establish wiring, not live GPT or semantic quality.</p>
<p><a href="README.md">Setup / tests / API</a> · <a href="WRITEUP.pdf">One-page write-up</a> · <a
href="docs/ASSIGNMENT_REQUIREMENTS.md">Requirements</a> · <a
href="{REPO}/tree/feat/langchain-langgraph">GitHub branch</a></p></section>
<section id="stack"><h2>Tech stack</h2><p>Python 3.11+, uv lock, LangChain create_agent /
LangGraph, ChatOpenAI, Pydantic, FastAPI / Uvicorn, Docker PostgreSQL / pgvector, pytest /
Ruff.</p>
<p>POST /triage: ticket or 1–100 unique tickets. Invalid input: 422; unavailable config: 503;
accepted results/fallback: 200. GET /health: liveness only. Loopback API 8000; DB
54329.</p></section>
<section id="spec"><h2>Specification, architecture, TODO and evidence</h2><p>Single maintained
planning source: <a href="plan.md">plan.md</a>. Tickets: <a href="{REPO}/issues/7">F01</a> → <a
href="{REPO}/issues/8">F02</a> → <a
href="{REPO}/issues/9">F03</a>.</p><pre>{escape(plan)}</pre></section>
<section id="original"><h2>Main Assignment — original Word text</h2><p>Faithful source text
follows. These are assignment requirements, distinct from the owner's implementation
choices.</p>{paragraphs}</section></main></html>
"""
    (ROOT / "ASSIGNMENT_READER.html").write_text(page, encoding="utf-8")


if __name__ == "__main__":
    main()
