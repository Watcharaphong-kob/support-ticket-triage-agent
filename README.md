> Framework branch: LangChain/LangGraph terminal migration is implemented. Live GPT credentials are required; --offline belongs to the original feat/triage-agent branch. API and final setup docs follow in F02/F03. Current specification and evidence: [plan.md](plan.md).

# Support Ticket Triage Agent

Phase 1 prototype for the **main Word assignment**: a Python CLI with an OpenAI GPT tool loop, customer-history lookup and Docker PostgreSQL/pgvector classic RAG. GraphRAG is deferred to Phase 2. The three original English/Thai conversations retain all twelve messages, relative times and supplied translations.

[Assignment reader](ASSIGNMENT_READER.html) · [Spec](docs/PROJECT_SPEC.md) · [TODO](docs/TODO.md) · [Tickets](docs/TICKETS.md) · [Main assignment traceability](docs/ASSIGNMENT_REQUIREMENTS.md) · [One-page write-up](WRITEUP.pdf) (editable [source](docs/WRITEUP.md)) · [Verification](docs/verification.md)

## Run the complete offline demonstration

For clone commands, expected output, assignment-fit assessment and live-vs-offline acceptance, see [Test guide](docs/TEST_GUIDE.md). The completed code is on `feat/triage-agent`; the older `main` branch is not the full prototype. The owner must grant access to this private repository before another person can clone it.

Prerequisites: Docker Desktop with Linux containers and Docker Compose. Run from the repository root. Compose loads `.env`; host Python reads environment variables only.

```powershell
Copy-Item .env.example .env
# Edit .env and replace POSTGRES_PASSWORD with your own local password.
docker compose up -d --build app
docker compose run --rm app python -m triage_agent.knowledge.manage ingest
docker compose run --rm app python -m triage_agent --input data/sample_tickets.json --offline --trace
docker compose run --rm -e TRIAGE_TEST_DATABASE=1 app python -m pytest -q -p no:cacheprovider
docker compose down
```

`--offline` requires EMBEDDING_BACKEND=fake and rejects live embedding configuration before any provider construction. It uses simple deterministic scenario rules and fake lexical embeddings. Output says `offline_demo`; it demonstrates wiring and policy, not GPT quality or semantic retrieval. The example knowledge/customer records are synthetic, allowed by the assignment. Nothing sends replies or changes accounts. Results include mock provenance and uncertainty. [Recorded samples](examples/sample_results.json) use the real database.

The app is a one-shot CLI container: a successful command exits. DB startup waits for health and repeatable migrations; knowledge persists in a named volume. The port binds only to `127.0.0.1:54329`. Keep the same password when reusing a volume. Tests create/drop a uniquely named temporary schema and preserve seeded demonstration articles.

## Run live GPT

Set your own `OPENAI_API_KEY` and `OPENAI_MODEL` in the ignored `.env`. Select an OpenAI GPT model supporting Chat Completions, function tools and JSON mode. Keys are never included in the submission. Then omit `--offline`:

```powershell
docker compose run --rm app python -m triage_agent --input data/sample_tickets.json --trace
```

GPT can use the existing fake-vector knowledge space for a tool-loop smoke test; output identifies the embedding model. For live semantic embeddings, create a **separate Compose project/database volume** and set `EMBEDDING_BACKEND=openai`, your chosen `EMBEDDING_MODEL`, supported `EMBEDDING_DIMENSION`, and key. Example project isolation:

```powershell
# After editing .env for live models, avoid the original project's host port.
$env:POSTGRES_PORT = '54330'
docker compose -p ooca-triage-live up -d --build app
docker compose -p ooca-triage-live run --rm app python -m triage_agent.knowledge.manage ingest
docker compose -p ooca-triage-live run --rm app python -m triage_agent --input data/sample_tickets.json --trace
docker compose -p ooca-triage-live down
Remove-Item Env:POSTGRES_PORT
```

Do not mix embedding models/dimensions in one database. Incompatible spaces are rejected, not silently reindexed. No paid/live checks were run during implementation; see [verification](docs/verification.md). HTTP contract tests cover both provider adapters. API usage follows the [OpenAI Chat Completions reference](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create).

## Develop with uv

Python 3.11+ (tested on 3.12), uv 0.12.6 and a running Compose DB:

```powershell
uv sync --locked
uv run --locked triage-agent --help
uv run --locked python -m triage_agent --version
uv run --locked python -m pytest -q
uv run --locked python -m ruff check src tests scripts
uv run --locked python -m ruff format --check src tests scripts
uv build
uv run --locked python scripts/build_planner.py
uv run --locked python scripts/check_delivery.py
```

Host tests skip DB integration unless `TRIAGE_TEST_DATABASE=1`. To run against Compose, set `PGHOST=127.0.0.1`, `PGPORT=54329`, `PGUSER=triage`, `PGDATABASE=triage`, `PGPASSWORD` to your local password, and `TRIAGE_TEST_DATABASE=1`. The full container command above is simpler and requires no host DB setup. CI performs host lint/delivery checks and the complete Docker test suite without paid keys.

## Input, output and tools

`--input` accepts one ticket object or a list of 1–100 unique tickets, following [sample input](data/sample_tickets.json) and `Ticket` in [schemas](src/triage_agent/schemas.py). `--customers` selects a synthetic customer fixture file. All fields are validated; original message order is retained.

Stdout contains one JSON object with `mode`, `embedding_model` and `results`. Each result contains urgency, product (null if unknown), issue_type, customer_sentiment, secondary_issues, next_action/destination, rationale, draft_response, knowledge_sources (retrieved chunk IDs), uncertainties, actual tool_calls, status and error. `--trace` writes safe tool status records to stderr. Exit codes: **0** all completed, **1** at least one fallback, **2** invalid input/configuration. Invalid batches fail before any ticket processing. Fallback never pretends successful classification.

[System prompt](prompts/system.txt) is packaged with the application; delivery-copy equality is checked. [Tools](src/triage_agent/tools.py) supply JSON schemas and implementations for `get_customer_history(customer_id)` and `search_knowledge_base(query, product?, issue_type?, locale?)`. History `not_found` discloses uncertainty; infrastructure errors fall back. Search is across languages unless explicitly filtered. Returned source/chunk IDs, excerpts, versions, locale, mock flag and scores provide provenance; similarity is not confidence. Empty search cannot justify auto-response.

The loop permits at most **6 model requests / 8 tool executions** per ticket, with 30-second provider timeouts, zero SDK retries and one shared transient retry/output correction. Parameterized read-only retrieval has 5-second connection/statement timeouts. Tools cannot execute shell commands, arbitrary SQL, URLs or billing changes. Application policy validates tool execution, citations, action/destination, low-urgency auto-response evidence and Thai draft language; prompt grounding remains fallible.

[Retrieval evaluation](docs/retrieval_evaluation.md) describes exact cosine top-five search, the prototype 0.2 cutoff, Unicode-safe section-aware 500-token chunks/60-token overlap, and live evaluation needed before production. [Knowledge spec](docs/AGENT_KNOWLEDGE_SPEC.md) describes embedding-space validation and Phase 2 boundaries.

Management commands: `python -m triage_agent.knowledge.manage migrate|ingest|stats|search|tool-demo`. Search accepts `--query`, `--locale`, `--product`, `--issue-type`. Example:

```powershell
docker compose run --rm app python -m triage_agent.knowledge.manage search --query 'payment charges' --issue-type billing
```

## Submission

The private [GitHub repository](https://github.com/Watcharaphong-kob/support-ticket-triage-agent) contains the delivery branch `feat/triage-agent`; use that branch for the completed prototype. Reviewer access is controlled by the repository owner. A source ZIP with an actual standalone `.git` directory is also provided locally as permitted by the Word assignment. It excludes `.env`, caches and virtual environments. Original Word content is transcribed in `docs/assignment_source.json`; it remains the main authority, distinct from selected architecture/policy choices.

## Repository layout

Runtime lives in `src/`, fixtures in `data/`, tests in `tests/`, and supporting documents in `docs/`. Open `ASSIGNMENT_READER.html` for the combined assignment/planner view. Ticket details are consolidated in [docs/TICKETS.md](docs/TICKETS.md), backed by the shared task registry and GitHub issues; individual generated ticket copies are no longer maintained. The submission PDF remains at the root.
