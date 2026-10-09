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
