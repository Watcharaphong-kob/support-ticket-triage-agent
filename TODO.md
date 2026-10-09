# Project TODO

9 October 2026 · 17/17 Phase 1 tasks done · Next: Phase 1 complete

[Spec](PROJECT_SPEC.md) · [Stack](TECH_STACK.md) · [Detailed planner](PROJECT_TASK_PLANNER.md)

[Tickets with skills, plugins and steps](TICKETS.md)

Checked tasks record completed setup/design and the user's E01 architecture decision. Classic RAG and Docker are selected for Phase 1; GraphRAG is deferred to Phase 2. Task data lives in docs/project_tasks.json; rebuild with uv run python scripts/build_planner.py.

## Design & setup

- [x] **T01 — Approve architecture and contracts** (done): Python CLI, urgency/action rubric, two tool contracts, output contract, and limits approved.

- [x] **T02 — Set up uv package and GitHub** (done): Both entry points run; safe environment config; 8 setup tests, Ruff and package builds pass; private repository pushed.



## Phase 1 decision

- [x] **E01 — Select Phase 1 prototype architecture** (done): User selected a Docker-based classic RAG prototype. PostgreSQL/pgvector and the existing OpenAI SDK approach define this phase; GraphRAG is Phase 2.



## Data & tools

- [x] **T03 — Create complete bilingual ticket fixtures** (done): All 3 tickets retain 4 messages, ordering, relative times, Thai and supplied translations; synthetic customer IDs labeled; no invented dates.

- [x] **T04 — Define validated input/tool/result contracts** (done): Invalid enums rejected; unknown product null; all approved fields present; completed/fallback rules and multi-issue input covered.

- [x] **T05 — Wire history and classic RAG tools** (done): Both tool schemas execute: fixture customer lookup and Docker PostgreSQL/pgvector KB retrieval; unknown customers, empty matches and DB errors explicit; mock knowledge flagged.

- [x] **T06 — Write grounded bilingual system prompt** (done): Whole-thread reasoning, severity/action policy, Thai draft replies, uncertainty, evidence references and untrusted-content rules included.



## Phase 1 RAG infrastructure

- [x] **E02 — Set up Docker Compose and PostgreSQL/pgvector** (done): App and PostgreSQL/pgvector services start through Compose; DB readiness and migrations verified; pinned image/dependencies; local named volume; secret-free example config.

- [x] **E03 — Implement classic RAG ingestion and embeddings** (done): English/Thai articles produce stable source/chunk IDs and idempotent upserts; configured embedding model/dimension/version validated; deterministic fake embeddings available for offline DB tests.

- [x] **E04 — Implement PostgreSQL classic RAG knowledge search** (done): Read-only parameterized top-5 vector retrieval returns source IDs/excerpts and provenance; locale/product filters, no-match and DB failure explicit; no graph traversal.



## Agent & decisions

- [x] **T07 — Build bounded GPT/tool execution loop** (done): Actual tool calls and results flow through adapter; both tools succeed before completed sample triage; timeout 30s, model requests <=6 and tool executions <=8 enforced.

- [x] **T08 — Apply action policy and integrate JSON CLI** (done): Action/destination and citations validated; failure escalates visibly; JSON stdout separated from optional stderr traces; batch exit status truthful.



## Phase 1 RAG verification

- [x] **E06 — Test classic RAG against Docker PostgreSQL** (done): Knowledge-tool contract and CLI/fake-model tests exercise real Docker pgvector using fake embeddings; bilingual source retrieval, re-ingestion, dimension mismatch, filters, citations, empty results and DB outage covered.



## Verification & delivery

- [x] **T09 — Verify scenarios and failure paths offline** (done): Three evidence-based sample cases, invalid output/citations, unknown tools, errors, exhausted budgets and injection attempts tested with fake model; no key required.

- [x] **T10 — Run demos and record live verification** (done): Compose sample run processes all three tickets; tool results/citations justified; mock embeddings/model runs labeled; live embeddings and GPT smoke verification reported separately.

- [x] **T11 — Finish README and one-page write-up** (done): README covers uv and Docker Compose, migrations, ingestion, tests and samples; one-page write-up describes prototype limits, implemented safeguards and production evaluation.

- [x] **T12 — Verify clean checkout and submit** (done): Clean-checkout commands succeed; offline CI documented/configured as selected; no secrets; reviewer access and final commit verified; ZIP fallback contains actual .git.



## Phase 2 â€” deferred GraphRAG

- [ ] **E05 — Explore GraphRAG in the next phase** (deferred): Future Phase 2 requires a reviewed graph schema, sourced relationships, bounded traversal and comparison against completed Phase 1 classic RAG; no Neo4j dependencies/services now.



## Before submission

Follow T12 acceptance and the final verification record. Verification covers fixtures, schemas, Docker, ingestion, retrieval, GPT adapter contracts, agent and CLI. Live provider calls have not run. The historical 210-minute estimate does not cover the expanded Phase 1 scope.
