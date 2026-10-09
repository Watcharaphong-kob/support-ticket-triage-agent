# Support Ticket Triage Agent

One LangChain agent running on LangGraph, with two read-only tools: customer history and classic RAG. The agent reads the full conversation, classifies urgency, extracts product/issue/sentiment, and proposes a draft response, specialist route or human escalation. Both terminal and API use the same code. Drafts are never sent.

## Setup and run

Requires Git, Docker Desktop with Compose, and your own OpenAI GPT key/model. Reviewers need access to this private repository.

```powershell
git clone https://github.com/Watcharaphong-kob/support-ticket-triage-agent.git
cd support-ticket-triage-agent
Copy-Item .env.example .env
# Edit .env: replace POSTGRES_PASSWORD and set OPENAI_API_KEY / OPENAI_MODEL.
docker compose up -d --build api
docker compose run --rm app python -m triage_agent.knowledge.manage ingest
docker compose run --rm app python -m triage_agent --input data/sample_tickets.json --trace
```

Use an OpenAI GPT model supporting Chat Completions and function calling. Compose loads `.env`; host Python reads exported shell variables. Run commands from the repository root. Migration runs before application startup; ingestion loads the supplied mock knowledge. Keep the DB password unchanged when reusing its volume.

### API

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
$json = Get-Content data/sample_tickets.json -Raw -Encoding utf8
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/triage -ContentType 'application/json; charset=utf-8' -Body ([Text.Encoding]::UTF8.GetBytes($json))
```

For bash: `curl -H 'Content-Type: application/json' --data-binary @data/sample_tickets.json http://127.0.0.1:8000/triage`.

[Swagger documentation](http://127.0.0.1:8000/docs) describes input schemas. API listens locally on port 8000; DB on 54329. Set `API_PORT` / `POSTGRES_PORT` in `.env` if occupied. `GET /health` reports process liveness, not model/DB readiness.

| Outcome | HTTP | CLI exit |
| --- | --- | --- |
| All tickets completed | 200 | 0 |
| Accepted batch with explicit per-ticket fallback | 200 | 1 |
| Invalid input, empty/oversized batch or duplicate IDs | 422 | 2 |
| Required runtime configuration unavailable | 503, sanitized | 2 |

Input accepts one ticket or 1–100 unique tickets. Validation precedes model/tool execution. Both transports return `mode`, `embedding_model` and `results`. CLI stdout contains JSON; `--trace` sends safe tool status/IDs to stderr. Failed triage returns explicit fallback to `human_support`, not fabricated completion.

### Local Python and smoke checks

With Python 3.11+ and uv installed:

```powershell
uv sync --locked --no-dev
uv run --locked --no-dev triage-agent --help
```

For host triage, export the OpenAI and PostgreSQL settings first; copying `.env` alone does not configure host Python. Docker is the recommended path.

Without paid credentials, verify startup, migration, ingestion and `/health` using the Docker commands above. `/triage` returns the documented 503 when GPT credentials are missing. Automated tests and planning files remain on [the development branch](https://github.com/Watcharaphong-kob/support-ticket-triage-agent/tree/feat/langchain-langgraph). Scripted tests establish wiring and safeguards; live GPT/semantic quality has not been evaluated.

## Tools and behavior

[Tool definitions and implementations](src/triage_agent/tools.py) expose:

- `get_customer_history(customer_id)`: required nonempty ID; additional arguments forbidden. Reads synthetic account/history fixtures and restricts access to the current ticket's customer. Returns `ok`, disclosed `not_found`, or sanitized `error`.
- `search_knowledge_base(query, product?, issue_type?, locale?)`: required nonempty query, maximum 8,000 characters; optional English/Thai locale. Read-only parameterized PostgreSQL/pgvector search returns up to five passages, actual source/chunk IDs, title, excerpt, version, locale, mock flag and similarity. Empty matches differ from failure.

[System prompt](src/triage_agent/prompts/system.txt) is the single packaged prompt. Argument/result schemas are in [schemas.py](src/triage_agent/schemas.py). Both real tools must execute before a completed result; the structured-output helper is not a third business tool. Application checks actual tool execution, customer scope and citation membership independently of model claims.

Results include urgency, product (null when unknown), issue type, sentiment, secondary issues, next action/destination, rationale, optional draft, citations, uncertainties and tool status. Critical incidents route to `incident_on_call` before billing; other billing cases require human review. Auto-response is only a supported low-urgency draft. Missing history and mock knowledge are disclosed; Thai tickets require Thai drafts.

Per ticket: six model requests, eight actual tool calls, 30-second GPT timeout, no automatic retries and 40 graph steps. Unknown/unauthorized calls, failed tools/provider, exhausted budgets or invalid output/citations cause visible fallback. No persistent memory, account changes or public deployment.

## Knowledge and configuration

`data/sample_tickets.json` preserves the three assignment conversations and all twelve messages, including Thai and supplied translations. IDs are synthetic. `data/customers.json` contains illustrative account context: null means unknown; customer reports are not verified billing/incident facts. `data/knowledge_base.json` contains illustrative policies, not actual company policy.

Default `fake-token-v1` embeddings are deterministic lexical vectors for setup, not proof of semantic RAG. For semantic retrieval, configure `EMBEDDING_BACKEND=openai`, compatible `EMBEDDING_MODEL` / `EMBEDDING_DIMENSION` and your own key. Use a separate Compose project/volume and free host ports to avoid mixing embedding spaces:

```powershell
# Edit .env for live embeddings first.
$env:POSTGRES_PORT = '54330'
$env:API_PORT = '8001'
docker compose -p ooca-triage-live up -d --build api
docker compose -p ooca-triage-live run --rm app python -m triage_agent.knowledge.manage ingest
docker compose -p ooca-triage-live run --rm app python -m triage_agent --input data/sample_tickets.json --trace
docker compose -p ooca-triage-live down
Remove-Item Env:POSTGRES_PORT, Env:API_PORT
```

`docker compose down` stops containers without deleting knowledge data. GraphRAG is deferred. Real knowledge, access controls and live evaluation are required before production.

## Deliverables

- Agent, CLI/API and classic RAG: `src/triage_agent/`, with runnable fixtures in `data/`.
- Environment: `.env.example`, `pyproject.toml`, `uv.lock`, Dockerfile and Compose setup.
- [System prompt](src/triage_agent/prompts/system.txt).
- [Tool definitions](src/triage_agent/tools.py).
- [One-page write-up](WRITEUP.pdf): architecture decisions, failure handling and production evaluation.
- This README: user setup, commands, configuration and expected outcomes.
