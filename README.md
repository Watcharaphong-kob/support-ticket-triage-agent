# Support Ticket Triage Agent

AI Engineer homework: an OpenAI GPT agent for support-ticket urgency, extraction, knowledge retrieval, and routing, including Thai and English conversations.

## Current status

Implemented through T05: faithful bilingual fixtures, validated contracts, Docker PostgreSQL/pgvector, ingestion and both read-only tools. The bounded GPT loop and triage prompt remain T06–T08 work. Providing --input to triage-agent still prints an explicit unfinished-processing error and exits with code 2.

Phase 1 is a Docker classic-RAG prototype. Fake lexical embeddings demonstrate database/tool contracts; they do not prove semantic or multilingual retrieval quality. An opt-in OpenAI embedding adapter is implemented, but no live provider check has run. GraphRAG is deferred to Phase 2.

## Docker setup and T05 demonstration

Prerequisites: Docker Desktop with Linux containers and Compose. Copy .env.example to an ignored .env and replace POSTGRES_PASSWORD with your own local password. Compose loads that file; the Python program itself uses environment variables only. Keep the same password for the existing named database volume.

```powershell
Copy-Item .env.example .env
# Edit .env: replace POSTGRES_PASSWORD before starting.
docker compose up -d --build app
docker compose run --rm app python -m triage_agent.knowledge.manage ingest
docker compose run --rm app python -m triage_agent.knowledge.manage tool-demo
docker compose run --rm app python -m triage_agent.knowledge.manage search --query "payment charges" --issue-type billing
docker compose run --rm -e TRIAGE_TEST_DATABASE=1 app python -m pytest -q -p no:cacheprovider
docker compose down
```

The database binds to 127.0.0.1:54329 by default and retains knowledge_data on stop. Startup waits for health and repeatable migrations. The app is a one-shot CLI container, so successful help/demo commands exit. No API key is needed with EMBEDDING_BACKEND=fake. Tests create and remove a uniquely named disposable schema; seeded demonstration articles remain intact. Compose configuration is tested on the host, since the app image does not contain Docker.

To use host uv commands against this database, set PGHOST=127.0.0.1, PGPORT=54329, PGUSER=triage, PGDATABASE=triage and PGPASSWORD to the same local password. Then run uv run --locked python -m triage_agent.knowledge.manage with the commands above.

For live embeddings, set EMBEDDING_BACKEND=openai, EMBEDDING_MODEL to your chosen compatible model, EMBEDDING_DIMENSION to its supported dimension and OPENAI_API_KEY. Ingest/query must use the same embedding space. Use a separate Compose project/database volume when switching from fake vectors; the existing space is deliberately rejected. Never silently mix models or delete a volume to resolve a mismatch. Provider calls have a 30-second timeout and no SDK retries. Queries/ingestion have five-second database statement/connect timeouts. Retrieval uses exact cosine similarity, a prototype 0.2 ranking cutoff, at most five passages, and metadata filters; tune the cutoff during live evaluation.

Images and Python dependencies are pinned by version and uv.lock. The embedding request/dimension contract follows [the official OpenAI reference](https://developers.openai.com/api/reference/python/resources/embeddings/methods/create); readiness follows [Compose guidance](https://docs.docker.com/compose/how-tos/startup-order/). See [pgvector documentation](https://github.com/pgvector/pgvector) and [uv Docker integration](https://docs.astral.sh/uv/guides/integration/docker/).

## Setup

Prerequisites: Git, uv, and Python 3.11 or later. The development default in .python-version is 3.12.

```powershell
git clone https://github.com/Watcharaphong-kob/support-ticket-triage-agent.git
cd support-ticket-triage-agent
uv sync --locked
uv run --locked triage-agent --help
uv run --locked python -m triage_agent --version
```

uv manages the local .venv. Commit pyproject.toml and uv.lock; do not commit the environment. For a supported locally installed Python version, use uv sync --locked --python 3.11 (or another supported version).

## Configuration

Help, version, and offline tests need no API key. Later live execution will require both OPENAI_API_KEY and OPENAI_MODEL, supplied by the runner. .env.example contains empty example values. Copying it to .env does not automatically load it; set variables in your shell. A real key must never be committed.

```powershell
$env:OPENAI_API_KEY = "your-own-key"
$env:OPENAI_MODEL = "your-selected-tool-capable-gpt-model"
```

On macOS/Linux, use export OPENAI_API_KEY and export OPENAI_MODEL. The config object hides the key from its repr and reports missing variable names without printing their values. No default model version is assumed.

## Verification

```powershell
uv run --locked pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
uv build
```

Tests cover setup, source fidelity, contracts, fake/live adapter HTTP boundaries, Unicode chunks, real PostgreSQL ingestion/retrieval and both tools. Host tests skip database integration unless TRIAGE_TEST_DATABASE=1 and PG variables are set. They do not verify the unimplemented GPT triage loop or live OpenAI calls. Build outputs go to ignored dist/.

Use uv add for runtime dependencies and uv add --dev for development tools. Commit the resulting pyproject.toml and uv.lock changes together. The [uv project guide](https://docs.astral.sh/uv/guides/projects/) explains locking and environment management.

## Planning documents

Task execution follows [the before/after checking workflow](docs/TASK_WORKFLOW.md): consult ask-matt, choose the appropriate implementation/testing/review route, and record evidence before marking tasks complete.

- PROJECT_TASK_PLANNER.md — tasks and acceptance criteria.
- PROJECT_SPEC.md — scope, policy, contracts, and acceptance in one current spec page.
- TECH_STACK.md — installed baseline and selected Phase 1 components.
- TODO.md — tech stack, spec checkpoints, and current working task list.
- TICKETS.md — each task's skills/plugins, simple steps, acceptance and evidence.
- docs/T05_IMPLEMENTATION_STATUS.md — verification, review fix and remaining scope.
- AGENT_KNOWLEDGE_SPEC.md — selected Docker/classic RAG contracts and deferred Phase 2 GraphRAG.
- GITHUB_REPO_PLAN.md — branches, worktrees, CI, submission.
- docs/superpowers/specs/2026-10-09-ticket-triage-design.md — approved design.
- ASSIGNMENT_READER.html — readable source and planning documents; opens offline.

Planner, TODO, and reader task statuses come from docs/project_tasks.json. Regenerate the documents with uv run --locked python scripts/build_planner.py. The reader has separate Spec and Tech Stack views; old original/spec/stack bookmarks remain supported. Source transcription is stored in docs/assignment_source.json so regeneration also works without the locally excluded DOCX.

The original DOCX stays local and is excluded from Git. The planning reader includes its textual transcription. The repository is private; give the evaluator access before submission. No actual API key is included.
