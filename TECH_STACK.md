# Tech Stack

9 October 2026 · Versions read from committed uv.lock

## Installed baseline

| Component | Technology | Version / choice | Status |
| --- | --- | --- | --- |
| Language | Python | >=3.11; development default 3.12 | Package ready |
| Packages | uv | pyproject.toml + uv.lock + ignored .venv | Ready |
| Model client | openai | 2.54.0 | GPT adapter implemented; mocked HTTP verified |
| Validation | pydantic | 2.14.0 | Installed; schemas T04 |
| CLI | argparse | Python standard library | JSON batch processing implemented |
| Tests | pytest | 9.1.1 | 8 setup tests passed at T02 |
| Lint / format | ruff | 0.16.10 | T02 checks passed |
| Build | setuptools | >=77 build backend | Wheel/source build verified |
| Source control | Git + private GitHub | main + feat/triage-agent | Repository ready |

## Selected Phase 1 components

| Area | Technology / decision | Status |
| --- | --- | --- |
| Main agent | openai SDK with explicit bounded tool loop | Implemented; 6 requests / 8 tool executions |
| Customer / ticket data | Synthetic UTF-8 JSON fixtures | T03 implemented |
| Runtime | Docker Engine 28.5.1 + Compose 2.40.0; Python 3.12.14 image + uv 0.12.6 | Startup verified |
| Knowledge database | PostgreSQL 17 + pgvector 0.8.7 | Healthy Docker service; migrations verified |
| Database client | psycopg 3.3.6 + pgvector 0.5.1 | uv-locked |
| Retrieval | Classic RAG; exact cosine search, top 5, metadata filters, 0.2 ranking cutoff | Real DB tests passed |
| Chunk tokenizer | tiktoken 0.14.0; cl100k_base | Unicode-safe 500 tokens / 60 overlap |
| Embeddings | Fake lexical vectors by default; opt-in OpenAI model/dimension | Adapter tested with mock HTTP; live semantic quality pending |
| Phase 2 | GraphRAG; backend decision in next phase | Deferred; no graph dependencies now |
| CI | GitHub Actions + uv offline checks | Configured; local-equivalent checks verified |

## Stack decisions

Phase 1 is a prototype using one knowledge database and the existing model SDK. Classic RAG retrieves passages; GraphRAG relationships and traversal belong to Phase 2. Pin compatible Docker images and new dependencies during setup. Details are in [knowledge-system spec](AGENT_KNOWLEDGE_SPEC.md).

## Configuration and commands

GPT model: OPENAI_MODEL. Key: OPENAI_API_KEY. No hard-coded model or actual key in the submission. Help/version/offline tests need no key.

```powershell
uv sync --locked
uv run --locked triage-agent --help
uv run --locked pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
uv build
uv run --locked python scripts/build_planner.py
```
