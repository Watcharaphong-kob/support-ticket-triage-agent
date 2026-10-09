# Execution Tickets

9 October 2026 · Local project tickets

Each ticket records dependencies, acceptance, skills/plugins and simple steps. Completed steps are evidence; planned steps are not claimed as executed.

[GitHub Phase 1 tracking issue](https://github.com/Watcharaphong-kob/support-ticket-triage-agent/issues/1) · closed — completed. The local task tickets below contain per-task execution details.

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

Plugins used: Superpowers: execution, review and verified delivery, GitHub: pushed private feature branch, opened draft PR #2, closed tracking issue #1, verified hosted CI.

Tools: PowerShell, uv, pytest, Ruff, Docker Compose. GitHub connector delivered PR/issue; hosted CI verified.

## Steps performed

1. Consulted ask-matt; verified independent review findings with failing regression tests.

2. Fixed offline live-embedding selection and Windows redirected Thai output; full rebuilt Docker suite passed.

3. Verified clean standalone clone with locked uv install, tests, package resources, Docker startup/ingestion/sample run and one-page PDF.

4. Configured pinned GitHub Actions and verified equivalent commands locally; packaged source plus actual standalone .git, excluding secrets/caches.

5. Regenerated planner/TODO/HTML, verified source fidelity and checked ask-matt after completion; repository delivery preserves main for review.

6. Pushed reviewed feature branch, attached draft PR #2, closed issue #1 and verified GitHub Actions push run success for 8d50edc.

## Verification

Final rebuilt Docker image: 65 passed/1 host-only skip; host Compose check passed. Fresh clone install and sdist/wheel builds pass; prompt/migration resources present; CLI regression 7 passed. Source+.git ZIP verified, no .env/caches. Independent standards findings fixed; spec 0 actionable. Remote CI reported separately. Live provider checks not run. Hosted GitHub Actions run 37904012936 succeeded for delivered commit 8d50edc.

Implementation commit: Reviewed implementation 614dfc0; delivery head recorded by Git and submission manifest..

## E05 — Explore GraphRAG in the next phase

Status: deferred. Scope: phase2. Dependencies: T12.

## Acceptance

Future Phase 2 requires a reviewed graph schema, sourced relationships, bounded traversal and comparison against completed Phase 1 classic RAG; no Neo4j dependencies/services now.

## Skills and plugins

Planned skills: ask-matt before/after, implement, tdd, code-review, Superpowers execution and verification. Not executed yet.

Planned plugins: Superpowers for implementation/verification; GitHub for execution evidence. Record actual usage after implementation.

## Planned steps

1. Read dependencies and acceptance; consult ask-matt.

2. Verify existing behavior through the agreed public seam; add a failing regression check only for a coverage gap.

3. Implement the smallest required change.

4. Consult ask-matt, test and review; record evidence before completion.

## S01 — Document testing, assignment fit and clone setup

Status: done. Scope: followup. Dependencies: T12.

## Acceptance

Four user questions answered with exact commands, pass criteria, honest Word-fit rating and reproducible private-repo setup; simplicity constraint documented.

## Skills and plugins

Skills used: ask-matt (before and after), grill-with-docs, grilling, domain-modeling, to-spec, superpowers:verification-before-completion.

Plugins used: Superpowers: evidence verification, GitHub: simplicity specification publication.

Tools: PowerShell, uv, pytest, Ruff, Docker Compose. GitHub connector delivered PR/issue; hosted CI verified.

## Steps performed

1. Consulted ask-matt and read the requested skills and current Word traceability.

2. Re-ran the complete Docker suite and inspected runtime size and README prerequisites.

3. Wrote reviewer test guide and simplicity spec; added follow-up tasks and HTML testing page.

4. Checked source fidelity, generator determinism and syntax; recorded live-quality limits separately.

5. Published simplicity spec as GitHub issue #3 with ready-for-agent; runtime refactor remains S02 TODO.

## Verification

Fresh Docker run: 65 passed, 1 host-only skip. Documentation/delivery checks and generator lint/syntax pass. No runtime code changed. Live checks remain unperformed.

Implementation commit: Follow-up documentation commit recorded by Git..

## S02 — Concentrate read-only tool validation

Status: todo. Scope: followup. Dependencies: S01.

[GitHub execution ticket](https://github.com/Watcharaphong-kob/support-ticket-triage-agent/issues/4)

[Parent specification](https://github.com/Watcharaphong-kob/support-ticket-triage-agent/issues/3) · ready-for-agent.

Publication complete: user approved both slices; to-tickets and ask-matt used; GitHub connector created the issue and native parent link was verified. Runtime implementation is pending.

## Acceptance

Keep ticket triage behavior unchanged while concentrating repeated tool-specific knowledge in the existing read-only tool module. The agent retains model turns, execution budgets, call IDs, transcript bookkeeping and fallback behavior.

- [ ] Remove repeated allowlist/validation knowledge only where total complexity decreases; record before/after code size and concepts.
- [ ] Preserve public ticket/result contracts and actual execution of customer-history and knowledge-search tools.
- [ ] Preserve failure timing and codes: malformed JSON, unknown tool, foreign customer and duplicate IDs remain rejected as currently tested; schema-invalid arguments remain a recorded tool error followed by tool_unavailable.
- [ ] Preserve currently rejected batch behavior, tool/model budgets, safe error details, trace records and grounded citations.
- [ ] Preserve full conversations, Thai output, missing-history disclosure and mock-knowledge labeling.
- [ ] Existing tests, full rebuilt Docker suite and host Compose checks pass; demonstrate all three source tickets through the JSON CLI.
- [ ] Update planner, TODO, reader HTML and ticket evidence. No generic registry, additional delegation module or new public seam solely to shorten a file.

## Skills and plugins

Planned skills: ask-matt before/after, implement, tdd, code-review, Superpowers execution and verification. Not executed yet.

Planned plugins: Superpowers for implementation/verification; GitHub for execution evidence. Record actual usage after implementation.

## Planned steps

1. Read dependencies and acceptance; consult ask-matt.

2. Verify existing behavior through the agreed public seam; add a failing regression check only for a coverage gap.

3. Implement the smallest required change.

4. Consult ask-matt, test and review; record evidence before completion.

## S03 — Simplify offline demonstration content

Status: todo. Scope: followup. Dependencies: S01.

[GitHub execution ticket](https://github.com/Watcharaphong-kob/support-ticket-triage-agent/issues/5)

[Parent specification](https://github.com/Watcharaphong-kob/support-ticket-triage-agent/issues/3) · ready-for-agent.

Publication complete: user approved both slices; to-tickets and ask-matt used; GitHub connector created the issue and native parent link was verified. Runtime implementation is pending.

## Acceptance

Make the offline demonstration implementation easier to read by reducing repeated scenario construction, while preserving the same model interface, sample results and explicit distinction from live GPT.

- [ ] Remove actual repeated logic or concepts; record before/after size and complexity. Moving a file or prose alone does not satisfy acceptance.
- [ ] Preserve the GPT and offline model adapters and existing public behavior; do not add an adapter hierarchy or loader framework.
- [ ] Preserve all three sample outcomes, whole-thread input, Thai drafts and separate secondary issues without hardcoding ticket IDs.
- [ ] Both tools still execute and citations still identify retrieved evidence; unknown scenarios retain honest limitations.
- [ ] Offline execution remains labeled and rejects live embedding configuration before constructing a paid provider.
- [ ] Existing tests, full rebuilt Docker suite and host Compose checks pass; demonstrate all three source tickets through the JSON CLI.
- [ ] If packaged data changes, verify installed wheel resources and fresh-clone execution.
- [ ] Update planner, TODO, reader HTML and ticket evidence. If no change reduces total complexity, record evidence and report it instead of accepting a cosmetic refactor.

## Skills and plugins

Planned skills: ask-matt before/after, implement, tdd, code-review, Superpowers execution and verification. Not executed yet.

Planned plugins: Superpowers for implementation/verification; GitHub for execution evidence. Record actual usage after implementation.

## Planned steps

1. Read dependencies and acceptance; consult ask-matt.

2. Verify existing behavior through the agreed public seam; add a failing regression check only for a coverage gap.

3. Implement the smallest required change.

4. Consult ask-matt, test and review; record evidence before completion.

## S04 — Tidy repository folders and consolidate ticket records

Status: done. Scope: followup. Dependencies: S01.

## Acceptance

Keep supporting Markdown documents under docs; consolidate duplicate local tickets without losing acceptance or evidence; fix relative links and rebuild checks; preserve Word, environment settings, runtime, tests and Git history.

## Skills and plugins

Skills used: ask-matt (before and after), superpowers:brainstorming (bounded cleanup approved), superpowers:verification-before-completion.

Plugins used: Superpowers: approved cleanup and evidence verification.

Tools: PowerShell, uv, pytest, Ruff, Docker Compose. No external app connector used for this task.

## Steps performed

1. Read tracked-file inventory and document references; proposed concrete cleanup and received approval.

2. Moved 11 supporting Markdown documents into docs; consolidated 21 generated ticket files into one maintained ticket record.

3. Updated task paths, README links, generator and source/link checks; retained runtime and submission requirements.

4. Rebuilt Docker image and ran full database suite; verified host Compose and package builds.

5. Verified deterministic reader generation and preserved Word source; synchronized primary folder and removed regenerable caches.

## Verification

Docker: 65 passed, 1 host-only skip. Host Compose: 1 passed. Wheel and sdist build succeeded. Ruff lint/format and reader/source checks passed; runtime code and tests unchanged.

Implementation commit: Cleanup commit recorded by Git..
