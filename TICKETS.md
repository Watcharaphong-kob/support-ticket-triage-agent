# Execution Tickets

9 October 2026 · Local project tickets

Each ticket records dependencies, acceptance, skills/plugins and simple steps. Completed steps are evidence; planned steps are not claimed as executed.

[GitHub Phase 1 tracking issue](https://github.com/Watcharaphong-kob/support-ticket-triage-agent/issues/1) · ready-for-agent. The local task tickets below contain per-task execution details.

## T01 — Approve architecture and contracts

Status: done. Scope: phase1. Dependencies: none.

## Acceptance

Python CLI, urgency/action rubric, two tool contracts, output contract, and limits approved.

## Skills and plugins

Historical task; skill usage was not recorded in this ticket format.

## Evidence

See the task outputs and existing setup/design evidence.

## T02 — Set up uv package and GitHub

Status: done. Scope: phase1. Dependencies: T01.

## Acceptance

Both entry points run; safe environment config; 8 setup tests, Ruff and package builds pass; private repository pushed.

## Skills and plugins

Historical task; skill usage was not recorded in this ticket format.

## Evidence

See the task outputs and existing setup/design evidence.

## E01 — Select Phase 1 prototype architecture

Status: done. Scope: phase1. Dependencies: T01.

## Acceptance

User selected a Docker-based classic RAG prototype. PostgreSQL/pgvector and the existing OpenAI SDK approach define this phase; GraphRAG is Phase 2.

## Skills and plugins

Historical task; skill usage was not recorded in this ticket format.

## Evidence

See the task outputs and existing setup/design evidence.

## T03 — Create complete bilingual ticket fixtures

Status: done. Scope: phase1. Dependencies: T02.

## Acceptance

All 3 tickets retain 4 messages, ordering, relative times, Thai and supplied translations; synthetic customer IDs labeled; no invented dates.

## Skills and plugins

Skills used: ask-matt (before and after), implement, tdd, superpowers:executing-plans, superpowers:using-git-worktrees, superpowers:verification-before-completion, code-review (standards and spec).

Plugins used: Superpowers: worktree, execution, debugging and verification workflow.

Tools: PowerShell, uv, pytest, Ruff, Docker Compose. No external app connector used for this task.

## Steps performed

1. Consulted ask-matt; reused the existing worktree and verified 8 setup tests.

2. Verified the independent DOCX transcription and wrote failing fixture checks.

3. Created all 12 original messages, supplied translations and synthetic customer links.

4. Ran source-fidelity tests; consulted ask-matt after implementation.

## Verification

Full Docker suite: 36 passed, 1 skipped (Compose check passed separately on host). Real PostgreSQL in disposable schemas; fake embeddings; mocked live adapter HTTP. Both tools succeeded for all 3 tickets. Ruff check/format passed. Standards review: 0 findings. Spec review: section-boundary finding fixed with a failing regression test, then green full suite. Live OpenAI calls not run.

Implementation commit: d61e1ca; review fix f82298b.

## T04 — Define validated input/tool/result contracts

Status: done. Scope: phase1. Dependencies: T03.

## Acceptance

Invalid enums rejected; unknown product null; all approved fields present; completed/fallback rules and multi-issue input covered.

## Skills and plugins

Skills used: ask-matt (before and after), implement, tdd, superpowers:executing-plans, superpowers:using-git-worktrees, superpowers:verification-before-completion, code-review (standards and spec).

Plugins used: Superpowers: worktree, execution, debugging and verification workflow.

Tools: PowerShell, uv, pytest, Ruff, Docker Compose. No external app connector used for this task.

## Steps performed

1. Consulted ask-matt and wrote failing input/result contract tests.

2. Added strict Pydantic ticket, customer, tool, knowledge and result contracts.

3. Validated nulls, enums, ordered messages, both-tool completion and fallback routing.

4. Ran the suite (21 passed at this checkpoint); consulted ask-matt after implementation.

## Verification

Full Docker suite: 36 passed, 1 skipped (Compose check passed separately on host). Real PostgreSQL in disposable schemas; fake embeddings; mocked live adapter HTTP. Both tools succeeded for all 3 tickets. Ruff check/format passed. Standards review: 0 findings. Spec review: section-boundary finding fixed with a failing regression test, then green full suite. Live OpenAI calls not run.

Implementation commit: d61e1ca; review fix f82298b.

## E02 — Set up Docker Compose and PostgreSQL/pgvector

Status: done. Scope: phase1. Dependencies: E01, T02.

## Acceptance

App and PostgreSQL/pgvector services start through Compose; DB readiness and migrations verified; pinned image/dependencies; local named volume; secret-free example config.

## Skills and plugins

Skills used: ask-matt (before and after), implement, tdd, superpowers:executing-plans, superpowers:using-git-worktrees, superpowers:verification-before-completion, code-review (standards and spec), superpowers:systematic-debugging.

Plugins used: Superpowers: worktree, execution, debugging and verification workflow.

Tools: PowerShell, uv, pytest, Ruff, Docker Compose. No external app connector used for this task.

## Steps performed

1. Consulted ask-matt and checked Compose readiness/storage configuration.

2. Added version-pinned Dockerfile, Compose database/app/migration services and uv dependencies.

3. Generated an ignored local password, started the database and fixed duplicate image build targets.

4. Verified healthy database, pgvector 0.8.7, CLI startup and repeatable migration; consulted ask-matt afterward.

## Verification

Full Docker suite: 36 passed, 1 skipped (Compose check passed separately on host). Real PostgreSQL in disposable schemas; fake embeddings; mocked live adapter HTTP. Both tools succeeded for all 3 tickets. Ruff check/format passed. Standards review: 0 findings. Spec review: section-boundary finding fixed with a failing regression test, then green full suite. Live OpenAI calls not run.

Implementation commit: d61e1ca; review fix f82298b.

## E03 — Implement classic RAG ingestion and embeddings

Status: done. Scope: phase1. Dependencies: E02.

## Acceptance

English/Thai articles produce stable source/chunk IDs and idempotent upserts; configured embedding model/dimension/version validated; deterministic fake embeddings available for offline DB tests.

## Skills and plugins

Skills used: ask-matt (before and after), implement, tdd, superpowers:executing-plans, superpowers:using-git-worktrees, superpowers:verification-before-completion, code-review (standards and spec), superpowers:systematic-debugging, openai-docs.

Plugins used: Superpowers: worktree, execution, debugging and verification workflow.

Tools: PowerShell, uv, pytest, Ruff, Docker Compose. No external app connector used for this task.

## Steps performed

1. Consulted ask-matt and wrote failing ingestion tests.

2. Added Unicode-safe 500-token chunks with 60-token overlap, stable hashes and atomic source replacement.

3. Added explicit fake embeddings and an opt-in OpenAI adapter with model/dimension checks.

4. Verified duplicate-free re-ingestion, Thai content, incompatible-space rejection and token limits; consulted ask-matt afterward.

5. Fixed the section-boundary finding: separate sections/paragraphs and repeat headings on long chunks; regression test RED then GREEN.

## Verification

Full Docker suite: 36 passed, 1 skipped (Compose check passed separately on host). Real PostgreSQL in disposable schemas; fake embeddings; mocked live adapter HTTP. Both tools succeeded for all 3 tickets. Ruff check/format passed. Standards review: 0 findings. Spec review: section-boundary finding fixed with a failing regression test, then green full suite. Live OpenAI calls not run.

Implementation commit: d61e1ca; review fix f82298b.

## E04 — Implement PostgreSQL classic RAG knowledge search

Status: done. Scope: phase1. Dependencies: E03, T04.

## Acceptance

Read-only parameterized top-5 vector retrieval returns source IDs/excerpts and provenance; locale/product filters, no-match and DB failure explicit; no graph traversal.

## Skills and plugins

Skills used: ask-matt (before and after), implement, tdd, superpowers:executing-plans, superpowers:using-git-worktrees, superpowers:verification-before-completion, code-review (standards and spec).

Plugins used: Superpowers: worktree, execution, debugging and verification workflow.

Tools: PowerShell, uv, pytest, Ruff, Docker Compose. No external app connector used for this task.

## Steps performed

1. Consulted ask-matt and wrote failing database-search tests.

2. Added parameterized read-only exact cosine retrieval with top-five bounds and metadata filters.

3. Returned document/chunk IDs, excerpts, version, mock flag and ranking score.

4. Verified citations, changed sources, safe filters, no-match and database failures; consulted ask-matt afterward.

## Verification

Full Docker suite: 36 passed, 1 skipped (Compose check passed separately on host). Real PostgreSQL in disposable schemas; fake embeddings; mocked live adapter HTTP. Both tools succeeded for all 3 tickets. Ruff check/format passed. Standards review: 0 findings. Spec review: section-boundary finding fixed with a failing regression test, then green full suite. Live OpenAI calls not run.

Implementation commit: d61e1ca; review fix f82298b.

## T05 — Wire history and classic RAG tools

Status: done. Scope: phase1. Dependencies: T03, T04, E04.

## Acceptance

Both tool schemas execute: fixture customer lookup and Docker PostgreSQL/pgvector KB retrieval; unknown customers, empty matches and DB errors explicit; mock knowledge flagged.

## Skills and plugins

Skills used: ask-matt (before and after), implement, tdd, superpowers:executing-plans, superpowers:using-git-worktrees, superpowers:verification-before-completion, code-review (standards and spec), to-spec (GitHub issue publication).

Plugins used: Superpowers: worktree, execution, debugging and verification workflow, GitHub: published Phase 1 spec/checkpoint issue #1 with ready-for-agent.

Tools: PowerShell, uv, pytest, Ruff, Docker Compose. GitHub connector published the tracking issue.

## Steps performed

1. Consulted ask-matt and wrote failing tool-dispatch tests.

2. Added allowlisted customer-history and database-search schemas plus implementations.

3. Ingested three synthetic KB articles and ran both tools for all three source tickets.

4. Ran the full Docker suite (35 passed, Compose host check separate); consulted ask-matt and requested standards/spec reviews.

5. Published the Phase 1 spec and implementation checkpoint as GitHub issue #1; code remains local and unpushed.

## Verification

Full Docker suite: 36 passed, 1 skipped (Compose check passed separately on host). Real PostgreSQL in disposable schemas; fake embeddings; mocked live adapter HTTP. Both tools succeeded for all 3 tickets. Ruff check/format passed. Standards review: 0 findings. Spec review: section-boundary finding fixed with a failing regression test, then green full suite. Live OpenAI calls not run.

Implementation commit: d61e1ca; review fix f82298b.

## T06 — Write grounded bilingual system prompt

Status: done. Scope: phase1. Dependencies: T04, T05.

## Acceptance

Whole-thread reasoning, severity/action policy, Thai draft replies, uncertainty, evidence references and untrusted-content rules included.

## Skills and plugins

Skills used: ask-matt (before and after), implement, tdd, superpowers:executing-plans, superpowers:verification-before-completion, code-review (final standards/spec review completed).

Plugins used: Superpowers: inline execution, debugging and verification.

Tools: PowerShell, uv, pytest, Ruff, Docker Compose. No external app connector used for this task.

## Steps performed

1. Consulted ask-matt and read the task acceptance before work.

2. Implemented write grounded bilingual system prompt at public prompt/model/policy/CLI seams.

3. Ran focused checks and real Docker database tests; recorded RED→GREEN corrections.

4. Consulted ask-matt after the task: verification passed; include this work in final two-axis review.

## Verification

Final Docker suite: 65 passed, 1 host-only skip; host Compose check passed separately. Standards review: 2 CLI findings fixed RED→GREEN; spec review: no actionable findings. No deferred minors. Live paid GPT/semantic embedding checks not run.

Implementation commit: Completion branch; final hash recorded in docs/verification.md.

## T07 — Build bounded GPT/tool execution loop

Status: done. Scope: phase1. Dependencies: T02, T04, T05, T06.

## Acceptance

Actual tool calls and results flow through adapter; both tools succeed before completed sample triage; timeout 30s, model requests <=6 and tool executions <=8 enforced.

## Skills and plugins

Skills used: ask-matt (before and after), implement, tdd, superpowers:executing-plans, superpowers:verification-before-completion, code-review (final standards/spec review completed).

Plugins used: Superpowers: inline execution, debugging and verification.

Tools: PowerShell, uv, pytest, Ruff, Docker Compose. No external app connector used for this task.

## Steps performed

1. Consulted ask-matt and read the task acceptance before work.

2. Implemented build bounded gpt/tool execution loop at public prompt/model/policy/CLI seams.

3. Ran focused checks and real Docker database tests; recorded RED→GREEN corrections.

4. Consulted ask-matt after the task: verification passed; include this work in final two-axis review.

## Verification

Final Docker suite: 65 passed, 1 host-only skip; host Compose check passed separately. Standards review: 2 CLI findings fixed RED→GREEN; spec review: no actionable findings. No deferred minors. Live paid GPT/semantic embedding checks not run.

Implementation commit: Completion branch; final hash recorded in docs/verification.md.

## T08 — Apply action policy and integrate JSON CLI

Status: done. Scope: phase1. Dependencies: T07.

## Acceptance

Action/destination and citations validated; failure escalates visibly; JSON stdout separated from optional stderr traces; batch exit status truthful.

## Skills and plugins

Skills used: ask-matt (before and after), implement, tdd, superpowers:executing-plans, superpowers:verification-before-completion, code-review (final standards/spec review completed).

Plugins used: Superpowers: inline execution, debugging and verification.

Tools: PowerShell, uv, pytest, Ruff, Docker Compose. No external app connector used for this task.

## Steps performed

1. Consulted ask-matt and read the task acceptance before work.

2. Implemented apply action policy and integrate json cli at public prompt/model/policy/CLI seams.

3. Ran focused checks and real Docker database tests; recorded RED→GREEN corrections.

4. Consulted ask-matt after the task: verification passed; include this work in final two-axis review.

## Verification

Final Docker suite: 65 passed, 1 host-only skip; host Compose check passed separately. Standards review: 2 CLI findings fixed RED→GREEN; spec review: no actionable findings. No deferred minors. Live paid GPT/semantic embedding checks not run.

Implementation commit: Completion branch; final hash recorded in docs/verification.md.

## E06 — Test classic RAG against Docker PostgreSQL

Status: done. Scope: phase1. Dependencies: E04.

## Acceptance

Knowledge-tool contract and CLI/fake-model tests exercise real Docker pgvector using fake embeddings; bilingual source retrieval, re-ingestion, dimension mismatch, filters, citations, empty results and DB outage covered.

## Skills and plugins

Skills used: ask-matt (before and after), implement, tdd, superpowers:executing-plans, superpowers:verification-before-completion, code-review (final standards/spec review completed).

Plugins used: Superpowers: inline execution, debugging and verification.

Tools: PowerShell, uv, pytest, Ruff, Docker Compose. No external app connector used for this task.

## Steps performed

1. Consulted ask-matt and read the task acceptance before work.

2. Implemented test classic rag against docker postgresql at public prompt/model/policy/CLI seams.

3. Ran focused checks and real Docker database tests; recorded RED→GREEN corrections.

4. Consulted ask-matt after the task: verification passed; include this work in final two-axis review.

## Verification

Final Docker suite: 65 passed, 1 host-only skip; host Compose check passed separately. Standards review: 2 CLI findings fixed RED→GREEN; spec review: no actionable findings. No deferred minors. Live paid GPT/semantic embedding checks not run.

Implementation commit: Completion branch; final hash recorded in docs/verification.md.

## T09 — Verify scenarios and failure paths offline

Status: done. Scope: phase1. Dependencies: T08, E06.

## Acceptance

Three evidence-based sample cases, invalid output/citations, unknown tools, errors, exhausted budgets and injection attempts tested with fake model; no key required.

## Skills and plugins

Skills used: ask-matt (before and after), implement, tdd, superpowers:executing-plans, superpowers:verification-before-completion, code-review (final standards/spec review completed).

Plugins used: Superpowers: inline execution, debugging and verification.

Tools: PowerShell, uv, pytest, Ruff, Docker Compose. No external app connector used for this task.

## Steps performed

1. Consulted ask-matt and read the task acceptance before work.

2. Implemented verify scenarios and failure paths offline at public prompt/model/policy/CLI seams.

3. Ran focused checks and real Docker database tests; recorded RED→GREEN corrections.

4. Consulted ask-matt after the task: verification passed; include this work in final two-axis review.

## Verification

Final Docker suite: 65 passed, 1 host-only skip; host Compose check passed separately. Standards review: 2 CLI findings fixed RED→GREEN; spec review: no actionable findings. No deferred minors. Live paid GPT/semantic embedding checks not run.

Implementation commit: Completion branch; final hash recorded in docs/verification.md.

## T10 — Run demos and record live verification

Status: done. Scope: phase1. Dependencies: T09.

## Acceptance

Compose sample run processes all three tickets; tool results/citations justified; mock embeddings/model runs labeled; live embeddings and GPT smoke verification reported separately.

## Skills and plugins

Skills used: ask-matt (before and after), implement, superpowers:executing-plans, superpowers:verification-before-completion.

Plugins used: Superpowers: execution and verification.

Tools: PowerShell, uv, pytest, Ruff, Docker Compose. No external app connector used for this task.

## Steps performed

1. Consulted ask-matt and checked the task acceptance.

2. Rebuilt the image and ran all three source tickets with real PostgreSQL and the labeled offline model.

3. Recorded samples and separate live-provider verification limits.

4. Consulted ask-matt after the task; artifact checks passed.

## Verification

Rebuilt image: 63 passed/1 host-only skip. All three offline sample results completed. Write-up PDF: exactly one page, rendered and inspected. Live provider checks not run.

Implementation commit: Completion branch; final delivery commit recorded in docs/verification.md.

## T11 — Finish README and one-page write-up

Status: done. Scope: phase1. Dependencies: T10.

## Acceptance

README covers uv and Docker Compose, migrations, ingestion, tests and samples; one-page write-up describes prototype limits, implemented safeguards and production evaluation.

## Skills and plugins

Skills used: ask-matt (before and after), implement, superpowers:executing-plans, superpowers:verification-before-completion, pdf:pdf.

Plugins used: Superpowers: execution and verification, PDF: authored/rendered one-page write-up.

Tools: PowerShell, uv, pytest, Ruff, Docker Compose. No external app connector used for this task.

## Steps performed

1. Consulted ask-matt and checked the task acceptance.

2. Wrote complete uv/Docker/live/offline/CLI/tool setup and run instructions.

3. Wrote the architecture, failure and evaluation write-up; generated and visually checked a one-page PDF.

4. Consulted ask-matt after the task; artifact checks passed.

## Verification

Rebuilt image: 63 passed/1 host-only skip. All three offline sample results completed. Write-up PDF: exactly one page, rendered and inspected. Live provider checks not run.

Implementation commit: Completion branch; final delivery commit recorded in docs/verification.md.

## T12 — Verify clean checkout and submit

Status: done. Scope: phase1. Dependencies: T11.

## Acceptance

Clean-checkout commands succeed; offline CI documented/configured as selected; no secrets; reviewer access and final commit verified; ZIP fallback contains actual .git.

## Skills and plugins

Skills used: ask-matt (before and after), implement, code-review (independent standards/spec agents), superpowers:executing-plans, superpowers:receiving-code-review, superpowers:verification-before-completion, superpowers:finishing-a-development-branch, pr, to-spec.

Plugins used: Superpowers: execution, review and verified delivery, GitHub: private feature-branch delivery and tracking issue.

Tools: PowerShell, uv, pytest, Ruff, Docker Compose. No external app connector used for this task.

## Steps performed

1. Consulted ask-matt; verified independent review findings with failing regression tests.

2. Fixed offline live-embedding selection and Windows redirected Thai output; full rebuilt Docker suite passed.

3. Verified clean standalone clone with locked uv install, tests, package resources, Docker startup/ingestion/sample run and one-page PDF.

4. Configured pinned GitHub Actions and verified equivalent commands locally; packaged source plus actual standalone .git, excluding secrets/caches.

5. Regenerated planner/TODO/HTML, verified source fidelity and checked ask-matt after completion; repository delivery preserves main for review.

## Verification

Final rebuilt Docker image: 65 passed/1 host-only skip; host Compose check passed. Fresh clone install and sdist/wheel builds pass; prompt/migration resources present; CLI regression 7 passed. Source+.git ZIP verified, no .env/caches. Independent standards findings fixed; spec 0 actionable. Remote CI reported separately. Live provider checks not run.

Implementation commit: Reviewed implementation 614dfc0; delivery head recorded by Git and submission manifest..

## E05 — Explore GraphRAG in the next phase

Status: deferred. Scope: phase2. Dependencies: T12.

## Acceptance

Future Phase 2 requires a reviewed graph schema, sourced relationships, bounded traversal and comparison against completed Phase 1 classic RAG; no Neo4j dependencies/services now.

## Skills and plugins

Planned skills: ask-matt before/after, implement, tdd, code-review, Superpowers execution and verification. Not executed yet.

## Planned steps

1. Read dependencies and acceptance; consult ask-matt.

2. Add a failing behavior check at the agreed public boundary.

3. Implement the smallest required change.

4. Consult ask-matt, test and review; record evidence before completion.
