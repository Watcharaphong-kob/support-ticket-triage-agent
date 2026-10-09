# Project TODO

9 October 2026 · 17/17 Phase 1 tasks done · Next: S02

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



## Reviewer guide and simplicity follow-up

- [x] **S01 — Document testing, assignment fit and clone setup** (done): Four user questions answered with exact commands, pass criteria, honest Word-fit rating and reproducible private-repo setup; simplicity constraint documented.

- [ ] **S02 — Concentrate read-only tool validation** (todo): Keep ticket triage behavior unchanged while concentrating repeated tool-specific knowledge in the existing read-only tool module. The agent retains model turns, execution budgets, call IDs, transcript bookkeeping and fallback behavior.

- [ ] Remove repeated allowlist/validation knowledge only where total complexity decreases; record before/after code size and concepts.
- [ ] Preserve public ticket/result contracts and actual execution of customer-history and knowledge-search tools.
- [ ] Preserve failure timing and codes: malformed JSON, unknown tool, foreign customer and duplicate IDs remain rejected as currently tested; schema-invalid arguments remain a recorded tool error followed by tool_unavailable.
- [ ] Preserve currently rejected batch behavior, tool/model budgets, safe error details, trace records and grounded citations.
- [ ] Preserve full conversations, Thai output, missing-history disclosure and mock-knowledge labeling.
- [ ] Existing tests, full rebuilt Docker suite and host Compose checks pass; demonstrate all three source tickets through the JSON CLI.
- [ ] Update planner, TODO, reader HTML and ticket evidence. No generic registry, additional delegation module or new public seam solely to shorten a file.

- [ ] **S03 — Simplify offline demonstration content** (todo): Make the offline demonstration implementation easier to read by reducing repeated scenario construction, while preserving the same model interface, sample results and explicit distinction from live GPT.

- [ ] Remove actual repeated logic or concepts; record before/after size and complexity. Moving a file or prose alone does not satisfy acceptance.
- [ ] Preserve the GPT and offline model adapters and existing public behavior; do not add an adapter hierarchy or loader framework.
- [ ] Preserve all three sample outcomes, whole-thread input, Thai drafts and separate secondary issues without hardcoding ticket IDs.
- [ ] Both tools still execute and citations still identify retrieved evidence; unknown scenarios retain honest limitations.
- [ ] Offline execution remains labeled and rejects live embedding configuration before constructing a paid provider.
- [ ] Existing tests, full rebuilt Docker suite and host Compose checks pass; demonstrate all three source tickets through the JSON CLI.
- [ ] If packaged data changes, verify installed wheel resources and fresh-clone execution.
- [ ] Update planner, TODO, reader HTML and ticket evidence. If no change reduces total complexity, record evidence and report it instead of accepting a cosmetic refactor.



## Before submission

Follow T12 acceptance and the final verification record. Verification covers fixtures, schemas, Docker, ingestion, retrieval, GPT adapter contracts, agent and CLI. Live provider calls have not run. The historical 210-minute estimate does not cover the expanded Phase 1 scope.
