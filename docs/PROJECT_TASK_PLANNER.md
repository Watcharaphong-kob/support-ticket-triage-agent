# Project Task Planner

9 October 2026 · Rebuilt from docs/project_tasks.json

## Current position

17 of 17 Phase 1 tasks complete. T01 design is approved; T02 setup is verified and pushed; E01 architecture selection is approved. Next ready task: S02. GPT/tool/CLI implementation is available; see verification for live-check limits.

This is the current task plan. Existing task IDs and completion evidence are preserved. Phase 1 is a Docker classic-RAG prototype using PostgreSQL + pgvector. GraphRAG is deferred to Phase 2. Selected components are not yet installed capabilities.

## Spec and stack

[Project spec](PROJECT_SPEC.md) defines scope, contracts and acceptance. [Tech stack](TECH_STACK.md) separates installed tools from selected Phase 1 components. [Working TODO list](TODO.md) mirrors the tasks below. [Execution tickets](TICKETS.md) record skills, plugins, steps and evidence. [RAG and GraphRAG spec](AGENT_KNOWLEDGE_SPEC.md) supplies extension details.

## Phases and timing

The original homework estimate was 210 minutes and the assignment recommends 150–240 minutes. Docker and real classic RAG expand that scope. A revised Phase 1 estimate is not assigned; original task minutes below are historical references, not a total for this prototype.

## Phase 1 — Docker classic RAG prototype

| Task | Status | Min | Dependencies | Deliverable |
| --- | --- | --- | --- | --- |
| T01 | done | 10 | — | Approve architecture and contracts |
| T02 | done | 10 | T01 | Set up uv package and GitHub |
| E01 | done | TBD | T01 | Select Phase 1 prototype architecture |
| T03 | done | 15 | T02 | Create complete bilingual ticket fixtures |
| T04 | done | 15 | T03 | Define validated input/tool/result contracts |
| E02 | done | TBD | E01, T02 | Set up Docker Compose and PostgreSQL/pgvector |
| E03 | done | TBD | E02 | Implement classic RAG ingestion and embeddings |
| E04 | done | TBD | E03, T04 | Implement PostgreSQL classic RAG knowledge search |
| T05 | done | 20 | T03, T04, E04 | Wire history and classic RAG tools |
| T06 | done | 15 | T04, T05 | Write grounded bilingual system prompt |
| T07 | done | 35 | T02, T04, T05, T06 | Build bounded GPT/tool execution loop |
| T08 | done | 20 | T07 | Apply action policy and integrate JSON CLI |
| E06 | done | TBD | E04 | Test classic RAG against Docker PostgreSQL |
| T09 | done | 25 | T08, E06 | Verify scenarios and failure paths offline |
| T10 | done | 15 | T09 | Run demos and record live verification |
| T11 | done | 20 | T10 | Finish README and one-page write-up |
| T12 | done | 10 | T11 | Verify clean checkout and submit |

## Phase 2 — deferred GraphRAG

| Task | Status | Dependencies | Deliverable |
| --- | --- | --- | --- |
| E05 | deferred | T12 | Explore GraphRAG in the next phase |

## Reviewer guide and simplicity follow-up

| Task | Status | Deliverable |
| --- | --- | --- |
| S01 | done | Document testing, assignment fit and clone setup |
| S02 | todo | Concentrate read-only tool validation |
| S03 | todo | Simplify offline demonstration content |
| S04 | done | Tidy repository folders and consolidate ticket records |

## Task contracts

### T01 — Approve architecture and contracts

Phase: Design & setup. Status: done. Depends on: none. Estimate: 10 min (historical).

Outputs: `docs/superpowers/specs/2026-10-09-ticket-triage-design.md`.

Acceptance: Python CLI, urgency/action rubric, two tool contracts, output contract, and limits approved.

### T02 — Set up uv package and GitHub

Phase: Design & setup. Status: done. Depends on: T01. Estimate: 10 min (historical).

Outputs: `pyproject.toml`, `uv.lock`, `src/triage_agent/cli.py`, `src/triage_agent/config.py`, `README.md`.

Acceptance: Both entry points run; safe environment config; 8 setup tests, Ruff and package builds pass; private repository pushed.

### E01 — Select Phase 1 prototype architecture

Phase: Phase 1 decision. Status: done. Depends on: T01. Estimate: TBD.

Outputs: `docs/AGENT_KNOWLEDGE_SPEC.md`.

Acceptance: User selected a Docker-based classic RAG prototype. PostgreSQL/pgvector and the existing OpenAI SDK approach define this phase; GraphRAG is Phase 2.

### T03 — Create complete bilingual ticket fixtures

Phase: Data & tools. Status: done. Depends on: T02. Estimate: 15 min (historical).

Outputs: `data/sample_tickets.json`, `data/customers.json`.

Acceptance: All 3 tickets retain 4 messages, ordering, relative times, Thai and supplied translations; synthetic customer IDs labeled; no invented dates.

Skills used: ask-matt (before and after), implement, tdd, superpowers:executing-plans, superpowers:using-git-worktrees, superpowers:verification-before-completion, code-review (standards and spec).

Plugins used: Superpowers: worktree, execution, debugging and verification workflow.

Verification: Full Docker suite: 36 passed, 1 skipped (Compose check passed separately on host). Real PostgreSQL in disposable schemas; fake embeddings; mocked live adapter HTTP. Both tools succeeded for all 3 tickets. Ruff check/format passed. Standards review: 0 findings. Spec review: section-boundary finding fixed with a failing regression test, then green full suite. Live OpenAI calls not run.

[Execution ticket](TICKETS.md)

### T04 — Define validated input/tool/result contracts

Phase: Data & tools. Status: done. Depends on: T03. Estimate: 15 min (historical).

Outputs: `src/triage_agent/schemas.py`, `tests/test_schemas.py`.

Acceptance: Invalid enums rejected; unknown product null; all approved fields present; completed/fallback rules and multi-issue input covered.

Skills used: ask-matt (before and after), implement, tdd, superpowers:executing-plans, superpowers:using-git-worktrees, superpowers:verification-before-completion, code-review (standards and spec).

Plugins used: Superpowers: worktree, execution, debugging and verification workflow.

Verification: Full Docker suite: 36 passed, 1 skipped (Compose check passed separately on host). Real PostgreSQL in disposable schemas; fake embeddings; mocked live adapter HTTP. Both tools succeeded for all 3 tickets. Ruff check/format passed. Standards review: 0 findings. Spec review: section-boundary finding fixed with a failing regression test, then green full suite. Live OpenAI calls not run.

[Execution ticket](TICKETS.md)

### E02 — Set up Docker Compose and PostgreSQL/pgvector

Phase: Phase 1 RAG infrastructure. Status: done. Depends on: E01, T02. Estimate: TBD.

Outputs: `compose.yaml`, `Dockerfile`, `pyproject.toml`, `uv.lock`, `migrations/`.

Acceptance: App and PostgreSQL/pgvector services start through Compose; DB readiness and migrations verified; pinned image/dependencies; local named volume; secret-free example config.

Skills used: ask-matt (before and after), implement, tdd, superpowers:executing-plans, superpowers:using-git-worktrees, superpowers:verification-before-completion, code-review (standards and spec), superpowers:systematic-debugging.

Plugins used: Superpowers: worktree, execution, debugging and verification workflow.

Verification: Full Docker suite: 36 passed, 1 skipped (Compose check passed separately on host). Real PostgreSQL in disposable schemas; fake embeddings; mocked live adapter HTTP. Both tools succeeded for all 3 tickets. Ruff check/format passed. Standards review: 0 findings. Spec review: section-boundary finding fixed with a failing regression test, then green full suite. Live OpenAI calls not run.

[Execution ticket](TICKETS.md)

### E03 — Implement classic RAG ingestion and embeddings

Phase: Phase 1 RAG infrastructure. Status: done. Depends on: E02. Estimate: TBD.

Outputs: `src/triage_agent/knowledge/ingest.py`, `tests/test_ingest.py`.

Acceptance: English/Thai articles produce stable source/chunk IDs and idempotent upserts; configured embedding model/dimension/version validated; deterministic fake embeddings available for offline DB tests.

Skills used: ask-matt (before and after), implement, tdd, superpowers:executing-plans, superpowers:using-git-worktrees, superpowers:verification-before-completion, code-review (standards and spec), superpowers:systematic-debugging, openai-docs.

Plugins used: Superpowers: worktree, execution, debugging and verification workflow.

Verification: Full Docker suite: 36 passed, 1 skipped (Compose check passed separately on host). Real PostgreSQL in disposable schemas; fake embeddings; mocked live adapter HTTP. Both tools succeeded for all 3 tickets. Ruff check/format passed. Standards review: 0 findings. Spec review: section-boundary finding fixed with a failing regression test, then green full suite. Live OpenAI calls not run.

[Execution ticket](TICKETS.md)

### E04 — Implement PostgreSQL classic RAG knowledge search

Phase: Phase 1 RAG infrastructure. Status: done. Depends on: E03, T04. Estimate: TBD.

Outputs: `src/triage_agent/knowledge/base.py`, `src/triage_agent/knowledge/postgres_store.py`, `tests/test_retrieval.py`.

Acceptance: Read-only parameterized top-5 vector retrieval returns source IDs/excerpts and provenance; locale/product filters, no-match and DB failure explicit; no graph traversal.

Skills used: ask-matt (before and after), implement, tdd, superpowers:executing-plans, superpowers:using-git-worktrees, superpowers:verification-before-completion, code-review (standards and spec).

Plugins used: Superpowers: worktree, execution, debugging and verification workflow.

Verification: Full Docker suite: 36 passed, 1 skipped (Compose check passed separately on host). Real PostgreSQL in disposable schemas; fake embeddings; mocked live adapter HTTP. Both tools succeeded for all 3 tickets. Ruff check/format passed. Standards review: 0 findings. Spec review: section-boundary finding fixed with a failing regression test, then green full suite. Live OpenAI calls not run.

[Execution ticket](TICKETS.md)

### T05 — Wire history and classic RAG tools

Phase: Data & tools. Status: done. Depends on: T03, T04, E04. Estimate: 20 min (historical).

Outputs: `src/triage_agent/tools.py`, `data/knowledge_base.json`, `tests/test_tools.py`.

Acceptance: Both tool schemas execute: fixture customer lookup and Docker PostgreSQL/pgvector KB retrieval; unknown customers, empty matches and DB errors explicit; mock knowledge flagged.

Skills used: ask-matt (before and after), implement, tdd, superpowers:executing-plans, superpowers:using-git-worktrees, superpowers:verification-before-completion, code-review (standards and spec), to-spec (GitHub issue publication).

Plugins used: Superpowers: worktree, execution, debugging and verification workflow, GitHub: published Phase 1 spec/checkpoint issue #1 with ready-for-agent.

Verification: Full Docker suite: 36 passed, 1 skipped (Compose check passed separately on host). Real PostgreSQL in disposable schemas; fake embeddings; mocked live adapter HTTP. Both tools succeeded for all 3 tickets. Ruff check/format passed. Standards review: 0 findings. Spec review: section-boundary finding fixed with a failing regression test, then green full suite. Live OpenAI calls not run.

[Execution ticket](TICKETS.md)

### T06 — Write grounded bilingual system prompt

Phase: Data & tools. Status: done. Depends on: T04, T05. Estimate: 15 min (historical).

Outputs: `prompts/system.txt`.

Acceptance: Whole-thread reasoning, severity/action policy, Thai draft replies, uncertainty, evidence references and untrusted-content rules included.

Skills used: ask-matt (before and after), implement, tdd, superpowers:executing-plans, superpowers:verification-before-completion, code-review (final standards/spec review completed).

Plugins used: Superpowers: inline execution, debugging and verification.

Verification: Final Docker suite: 65 passed, 1 host-only skip; host Compose check passed separately. Standards review: 2 CLI findings fixed RED→GREEN; spec review: no actionable findings. No deferred minors. Live paid GPT/semantic embedding checks not run.

[Execution ticket](TICKETS.md)

### T07 — Build bounded GPT/tool execution loop

Phase: Agent & decisions. Status: done. Depends on: T02, T04, T05, T06. Estimate: 35 min (historical).

Outputs: `src/triage_agent/agent.py`, `tests/test_agent.py`.

Acceptance: Actual tool calls and results flow through adapter; both tools succeed before completed sample triage; timeout 30s, model requests <=6 and tool executions <=8 enforced.

Skills used: ask-matt (before and after), implement, tdd, superpowers:executing-plans, superpowers:verification-before-completion, code-review (final standards/spec review completed).

Plugins used: Superpowers: inline execution, debugging and verification.

Verification: Final Docker suite: 65 passed, 1 host-only skip; host Compose check passed separately. Standards review: 2 CLI findings fixed RED→GREEN; spec review: no actionable findings. No deferred minors. Live paid GPT/semantic embedding checks not run.

[Execution ticket](TICKETS.md)

### T08 — Apply action policy and integrate JSON CLI

Phase: Agent & decisions. Status: done. Depends on: T07. Estimate: 20 min (historical).

Outputs: `src/triage_agent/policy.py`, `src/triage_agent/cli.py`, `tests/test_policy.py`.

Acceptance: Action/destination and citations validated; failure escalates visibly; JSON stdout separated from optional stderr traces; batch exit status truthful.

Skills used: ask-matt (before and after), implement, tdd, superpowers:executing-plans, superpowers:verification-before-completion, code-review (final standards/spec review completed).

Plugins used: Superpowers: inline execution, debugging and verification.

Verification: Final Docker suite: 65 passed, 1 host-only skip; host Compose check passed separately. Standards review: 2 CLI findings fixed RED→GREEN; spec review: no actionable findings. No deferred minors. Live paid GPT/semantic embedding checks not run.

[Execution ticket](TICKETS.md)

### E06 — Test classic RAG against Docker PostgreSQL

Phase: Phase 1 RAG verification. Status: done. Depends on: E04. Estimate: TBD.

Outputs: `tests/test_retrieval.py`, `docs/retrieval_evaluation.md`.

Acceptance: Knowledge-tool contract and CLI/fake-model tests exercise real Docker pgvector using fake embeddings; bilingual source retrieval, re-ingestion, dimension mismatch, filters, citations, empty results and DB outage covered.

Skills used: ask-matt (before and after), implement, tdd, superpowers:executing-plans, superpowers:verification-before-completion, code-review (final standards/spec review completed).

Plugins used: Superpowers: inline execution, debugging and verification.

Verification: Final Docker suite: 65 passed, 1 host-only skip; host Compose check passed separately. Standards review: 2 CLI findings fixed RED→GREEN; spec review: no actionable findings. No deferred minors. Live paid GPT/semantic embedding checks not run.

[Execution ticket](TICKETS.md)

### T09 — Verify scenarios and failure paths offline

Phase: Verification & delivery. Status: done. Depends on: T08, E06. Estimate: 25 min (historical).

Outputs: `tests/test_agent.py`, `tests/test_policy.py`, `tests/test_tools.py`.

Acceptance: Three evidence-based sample cases, invalid output/citations, unknown tools, errors, exhausted budgets and injection attempts tested with fake model; no key required.

Skills used: ask-matt (before and after), implement, tdd, superpowers:executing-plans, superpowers:verification-before-completion, code-review (final standards/spec review completed).

Plugins used: Superpowers: inline execution, debugging and verification.

Verification: Final Docker suite: 65 passed, 1 host-only skip; host Compose check passed separately. Standards review: 2 CLI findings fixed RED→GREEN; spec review: no actionable findings. No deferred minors. Live paid GPT/semantic embedding checks not run.

[Execution ticket](TICKETS.md)

### T10 — Run demos and record live verification

Phase: Verification & delivery. Status: done. Depends on: T09. Estimate: 15 min (historical).

Outputs: `examples/sample_results.json`, `docs/verification.md`.

Acceptance: Compose sample run processes all three tickets; tool results/citations justified; mock embeddings/model runs labeled; live embeddings and GPT smoke verification reported separately.

Skills used: ask-matt (before and after), implement, superpowers:executing-plans, superpowers:verification-before-completion.

Plugins used: Superpowers: execution and verification.

Verification: Rebuilt image: 63 passed/1 host-only skip. All three offline sample results completed. Write-up PDF: exactly one page, rendered and inspected. Live provider checks not run.

[Execution ticket](TICKETS.md)

### T11 — Finish README and one-page write-up

Phase: Verification & delivery. Status: done. Depends on: T10. Estimate: 20 min (historical).

Outputs: `README.md`, `docs/WRITEUP.md`, `WRITEUP.pdf`.

Acceptance: README covers uv and Docker Compose, migrations, ingestion, tests and samples; one-page write-up describes prototype limits, implemented safeguards and production evaluation.

Skills used: ask-matt (before and after), implement, superpowers:executing-plans, superpowers:verification-before-completion, pdf:pdf.

Plugins used: Superpowers: execution and verification, PDF: authored/rendered one-page write-up.

Verification: Rebuilt image: 63 passed/1 host-only skip. All three offline sample results completed. Write-up PDF: exactly one page, rendered and inspected. Live provider checks not run.

[Execution ticket](TICKETS.md)

### T12 — Verify clean checkout and submit

Phase: Verification & delivery. Status: done. Depends on: T11. Estimate: 10 min (historical).

Outputs: `.github/workflows/ci.yml`, `docs/verification.md`.

Acceptance: Clean-checkout commands succeed; offline CI documented/configured as selected; no secrets; reviewer access and final commit verified; ZIP fallback contains actual .git.

Skills used: ask-matt (before and after), implement, code-review (independent standards/spec agents), superpowers:executing-plans, superpowers:receiving-code-review, superpowers:verification-before-completion, superpowers:finishing-a-development-branch, pr, to-spec.

Plugins used: Superpowers: execution, review and verified delivery, GitHub: pushed private feature branch, opened draft PR #2, closed tracking issue #1, verified hosted CI.

Verification: Final rebuilt Docker image: 65 passed/1 host-only skip; host Compose check passed. Fresh clone install and sdist/wheel builds pass; prompt/migration resources present; CLI regression 7 passed. Source+.git ZIP verified, no .env/caches. Independent standards findings fixed; spec 0 actionable. Remote CI reported separately. Live provider checks not run. Hosted GitHub Actions run 37904012936 succeeded for delivered commit 8d50edc.

[Execution ticket](TICKETS.md)

### E05 — Explore GraphRAG in the next phase

Phase: Phase 2 â€” deferred GraphRAG. Status: deferred. Depends on: T12. Estimate: TBD.

Outputs: `src/triage_agent/knowledge/neo4j_store.py`, `tests/test_graph_retrieval.py`.

Acceptance: Future Phase 2 requires a reviewed graph schema, sourced relationships, bounded traversal and comparison against completed Phase 1 classic RAG; no Neo4j dependencies/services now.

### S01 — Document testing, assignment fit and clone setup

Phase: Reviewer guide and simplicity follow-up. Status: done. Depends on: T12. Estimate: TBD.

Outputs: `docs/TEST_GUIDE.md`, `docs/SIMPLICITY_SPEC.md`, `ASSIGNMENT_READER.html`.

Acceptance: Four user questions answered with exact commands, pass criteria, honest Word-fit rating and reproducible private-repo setup; simplicity constraint documented.

Skills used: ask-matt (before and after), grill-with-docs, grilling, domain-modeling, to-spec, superpowers:verification-before-completion.

Plugins used: Superpowers: evidence verification, GitHub: simplicity specification publication.

Verification: Fresh Docker run: 65 passed, 1 host-only skip. Documentation/delivery checks and generator lint/syntax pass. No runtime code changed. Live checks remain unperformed.

[Execution ticket](TICKETS.md)

### S02 — Concentrate read-only tool validation

Phase: Reviewer guide and simplicity follow-up. Status: todo. Depends on: S01. Estimate: TBD.

Outputs: `src/triage_agent/agent.py`, `src/triage_agent/tools.py`, `tests/test_agent.py`, `ASSIGNMENT_READER.html`.

Acceptance: Keep ticket triage behavior unchanged while concentrating repeated tool-specific knowledge in the existing read-only tool module. The agent retains model turns, execution budgets, call IDs, transcript bookkeeping and fallback behavior.

- [ ] Remove repeated allowlist/validation knowledge only where total complexity decreases; record before/after code size and concepts.
- [ ] Preserve public ticket/result contracts and actual execution of customer-history and knowledge-search tools.
- [ ] Preserve failure timing and codes: malformed JSON, unknown tool, foreign customer and duplicate IDs remain rejected as currently tested; schema-invalid arguments remain a recorded tool error followed by tool_unavailable.
- [ ] Preserve currently rejected batch behavior, tool/model budgets, safe error details, trace records and grounded citations.
- [ ] Preserve full conversations, Thai output, missing-history disclosure and mock-knowledge labeling.
- [ ] Existing tests, full rebuilt Docker suite and host Compose checks pass; demonstrate all three source tickets through the JSON CLI.
- [ ] Update planner, TODO, reader HTML and ticket evidence. No generic registry, additional delegation module or new public seam solely to shorten a file.

### S03 — Simplify offline demonstration content

Phase: Reviewer guide and simplicity follow-up. Status: todo. Depends on: S01. Estimate: TBD.

Outputs: `src/triage_agent/models.py`, `tests/test_end_to_end.py`, `ASSIGNMENT_READER.html`.

Acceptance: Make the offline demonstration implementation easier to read by reducing repeated scenario construction, while preserving the same model interface, sample results and explicit distinction from live GPT.

- [ ] Remove actual repeated logic or concepts; record before/after size and complexity. Moving a file or prose alone does not satisfy acceptance.
- [ ] Preserve the GPT and offline model adapters and existing public behavior; do not add an adapter hierarchy or loader framework.
- [ ] Preserve all three sample outcomes, whole-thread input, Thai drafts and separate secondary issues without hardcoding ticket IDs.
- [ ] Both tools still execute and citations still identify retrieved evidence; unknown scenarios retain honest limitations.
- [ ] Offline execution remains labeled and rejects live embedding configuration before constructing a paid provider.
- [ ] Existing tests, full rebuilt Docker suite and host Compose checks pass; demonstrate all three source tickets through the JSON CLI.
- [ ] If packaged data changes, verify installed wheel resources and fresh-clone execution.
- [ ] Update planner, TODO, reader HTML and ticket evidence. If no change reduces total complexity, record evidence and report it instead of accepting a cosmetic refactor.

### S04 — Tidy repository folders and consolidate ticket records

Phase: Reviewer guide and simplicity follow-up. Status: done. Depends on: S01. Estimate: TBD.

Outputs: `README.md`, `docs/TICKETS.md`, `scripts/build_planner.py`, `scripts/check_delivery.py`, `ASSIGNMENT_READER.html`.

Acceptance: Keep supporting Markdown documents under docs; consolidate duplicate local tickets without losing acceptance or evidence; fix relative links and rebuild checks; preserve Word, environment settings, runtime, tests and Git history.

Skills used: ask-matt (before and after), superpowers:brainstorming (bounded cleanup approved), superpowers:verification-before-completion.

Plugins used: Superpowers: approved cleanup and evidence verification.

Verification: Docker: 65 passed, 1 host-only skip. Host Compose: 1 passed. Wheel and sdist build succeeded. Ruff lint/format and reader/source checks passed; runtime code and tests unchanged.

[Execution ticket](TICKETS.md)

## Execution rules

Implement one task at a time in dependency order. Use focused failing tests before behavior changes and record actual verification. Keep prompts/tools/model adapters separate. Do not mark installed libraries as working agent features. Review architecture changes before extension implementation.

Consult ask-matt before and after each task to select the testing/review route. Record fresh evidence before marking completion; see docs/TASK_WORKFLOW.md. The completed T03 plan is docs/superpowers/plans/2026-10-09-t03-bilingual-fixtures.md; next ready task: S02.

T02 evidence: docs/T02_SETUP_STATUS.md. Repository/worktree/submission workflow: [GitHub plan](GITHUB_REPO_PLAN.md). Preserve customer uncertainty and source citations.
