# Execution ledger — plan: docs/project_tasks.json

Baseline: 8ce5722. Original Word assignment is the main authority. User authorized continuous completion on 9 October 2026.

Preflight T06→T07→T08: packaged prompt feeds adapter; existing Chat Completions tool definitions feed the bounded loop; actual tool records and retrieved evidence feed final validation. T08→E06/T09→T10→T11→T12: public CLI is the test/delivery seam.

Ruling: adopt the three interview recommendations under the user's continuous-completion instruction: mock sources permit only labeled demonstration drafts; search across languages by default; missing history permits disclosed uncertainty, but tool failure triggers fallback. These preserve the prototype scope; different preferences require a small policy change.

Ruling: no provider credentials are available. Deliver the live GPT adapter plus mocked HTTP tests and labeled offline sample runs; disclose that paid live verification remains unperformed. Offline tests cannot establish live model quality.

T06 before: ask-matt → implement/TDD; original Word checked, full baseline 36 passed/1 skipped. T07 before: same route, scripted model public seam. T08 before: same route, CLI/policy public seams. Final two-axis review covers the whole completion range; task checks run at each checkpoint.

T06 complete: packaged bilingual prompt + identical delivery copy; prompt supplied with complete thread in agent checks. Ask-matt after → verification/final review.
T07 complete: public agent and mocked HTTP SDK checks passed, six-request/eight-tool ceilings and shared one-retry budget tested. Ask-matt after → verification/final review.
T08 complete: CLI RED (missing offline/processing) → GREEN; high-urgency auto-response regression RED → GREEN; JSON/traces/exit codes checked. Ask-matt after → verification/final review.
E06 before: ask-matt → real DB integration. Complete: disposable PostgreSQL schema, three sample citations, CLI and outage checks pass. Test assumed semantic chunk IDs; actual IDs are hashes, corrected assertion to verify retrieved document-to-chunk membership. Ask-matt after → verification/final review.
T09 before: ask-matt → failure-path TDD. Complete: unknown tool, foreign customer, bad arguments, duplicate IDs, invalid output/citations, injection allowlist, missing history, provider/tool errors and budgets checked. Ask-matt after → verification/final review.
T10 before: ask-matt → sample runs/verification. T11 before: ask-matt → delivery documentation. T12 before: ask-matt → clean-checkout/CI/final two-axis review.

T10 complete: rebuilt image suite 63 passed/1 skip; all three sample results recorded as offline_demo/fake-token-v1, actual both-tool records and citations. Ask-matt after → artifact verification passed.
T11 complete: README includes reproducible commands and live limits; WRITEUP PDF exactly one page, rendered and visually inspected. Ask-matt after → delivery documentation checks passed.

Final standards: 2 important CLI findings. Final spec: 0 actionable findings. Final fixed live embeddings under --offline — test_offline_rejects_live_embedding_configuration_before_constructing_provider RED→GREEN. Final fixed Windows Thai redirected JSON/traces — test_redirected_windows_encoding_preserves_unicode_json RED→GREEN. Whole Docker suite 65 passed/1 host-only skip.
Final: Ruling: reviewers declined live model/retrieval/semantic injection quality — retain explicit unverified status because no paid credentials are available — cost: future live evaluation may uncover quality issues.
Final: Ruling: reviewers declined T12 and remote CI — directly verify clean clone and delivery, report remote CI separately — cost: hosted-runner differences may require adjustments.

T12 complete: clean standalone clone uv install/build, Docker migrate/ingest/full suite/sample runs, resource/reader/PDF checks and source+.git ZIP all verified. Final rebuilt image 65 passed/1 host-only skip; Compose check passes on host. Ask-matt after → verified submission and final review complete.
Ruling: deliver the reviewed feature branch without merging main, plus source+.git ZIP — user authorized continuous repository/project delivery; no destructive integration is needed — cost: repository consumers must choose the delivery branch until integration.
Ruling: private evaluator access cannot be confirmed without an identity; retain privacy and provide the permitted standalone ZIP — cost: URL-only submission needs the owner to grant access.

Delivery verified: 8d50edc pushed; draft PR #2 attached; issue #1 closed; hosted CI run 37904012936 succeeded. Ask-matt post-task check: full prototype completion verified; live quality limitations retained.

S01 before: ask-matt → grill-with-docs facts + to-spec synthesis, reuse approved CLI/DB test seams. Fact subagent unavailable; read/count current sources directly. Docker suite 65 passed/1 host-only skip. User requests simplicity; interpretation recorded as readable minimal concepts without dropping required behavior. S01 after: ask-matt → documentation/source/syntax verification. Runtime untouched; S02 simplification proposed separately.


Architecture ticket publication before: ask-matt → improve-codebase-architecture/codebase-design survey → to-tickets. User accepted both slices. Published S02/#4 and S03/#5 with ready-for-agent; verified native sub-issue parent #3, labels/open states and unchanged parent body. S01 is complete; no dependency between these tickets. Regenerated planner/TODO/tickets/HTML; runtime untouched. Post-task ask-matt route: verify published acceptance/blockers and deterministic source-fidelity checks; implementation/TDD/review is later work.

Repository cleanup before: ask-matt -> bounded approved cleanup. Moved 11 supporting Markdown documents into docs and removed 21 duplicate generated ticket files; combined TICKETS.md, registry and GitHub issues retain all task acceptance/evidence. Updated generator, links, metadata and delivery assertions. Preserved runtime, tests, Word original, environment settings and Git history. After: ask-matt -> source fidelity, deterministic generation, relative-link checks, lint/package/Docker verification. S02/S03 runtime refactors remain pending.

Fresh cleanup checks: Docker rebuild succeeded, full suite 65 passed/1 host-only skip; host Compose 1 passed. Wheel/sdist build succeeded with network access after sandbox PyPI DNS failure. Ruff lint/format and reader/source checks passed. No runtime or test edits.

Specification refresh before: ask-matt -> to-spec synthesis of approved architecture tickets and completed cleanup. Reused previously approved CLI/tool/database seams; no new decision or interview. Updated existing specification and tracking issue rather than creating duplicate files/issues. After: ask-matt -> seven-section/template, status, publication, source-fidelity and deterministic-reader verification. Runtime unchanged.
