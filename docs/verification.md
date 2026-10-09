# Phase 1 verification — 9 October 2026

Authority: original Word assignment, with user-selected Docker/classic-RAG prototype scope. GraphRAG remains deferred.

- Rebuilt Docker image without source mounts: **65 passed, 1 skipped**. The skipped test needs the host Docker CLI; it is verified separately on the host.
- Agent/model/policy/CLI focused suite: **29 passed**. Ruff check and formatting pass.
- Real PostgreSQL/pgvector ingestion and all three sample triage runs succeed. `examples/sample_results.json` is explicitly `offline_demo` with `fake-token-v1` embeddings. This is not a live GPT result or a model-quality benchmark.
- Sample 1: high → billing_payments; sample 2: critical → incident_on_call, Thai draft; sample 3: low → product_support, with scheduling request retained. These are project policy expectations, not an official assignment answer key.
- Both tools execute for each sample. Citations refer to actual returned chunk IDs; mock provenance and unresolved facts remain visible.
- OpenAI GPT and embedding adapters are exercised with mocked HTTP. **Paid/live GPT and semantic embedding checks were not run:** no API key/model was configured. README provides the exact opt-in commands.
- Fresh standards/spec review, clean-checkout build/tests, package-resource check, HTML checks, GitHub delivery and final commit evidence are added below as executed.

Test schemas are disposable; demonstration data remains in the public schema. Local .env, virtual environments, caches and private credentials are excluded from delivery. Actual provider exception content and tool arguments are omitted from traces.

Final independent reviews: standards identified two CLI defects, both regression-tested RED→GREEN; spec identified no actionable gaps. See docs/FINAL_REVIEW.md. No deferred minor findings.

Clean standalone clone: uv sync --locked succeeded; host suite before review fixes 56 passed/8 database skips; sdist/wheel builds succeeded with packaged prompt/migration; full Docker suite before fixes 63 passed/1 skip, plus ingestion and all three sample runs. The review-fix suite is 65 passed/1 skip and is rebuilt/rechecked below before delivery. Host Compose check, Ruff check/format, deterministic planner regeneration, 35-paragraph source fidelity and reader JavaScript syntax pass. The write-up PDF is exactly one page, visually inspected and re-read from the clone.

Final rebuilt image (review fixes, no source mounts): **65 passed, 1 skipped**; host Compose check independently passed. Clean clone public CLI regression: **7 passed**. Reviewed code commit: **614dfc0**. Source+.git ZIP verified as a standalone repository (no commondir or alternates), with no .env, virtual environment or cache. GitHub remains private; no evaluator identity was supplied, so URL-only evaluator access cannot be confirmed. The ZIP provides the assignment-permitted alternative without changing repository visibility.

Repository delivery: private feat/triage-agent pushed successfully; [draft PR #2](https://github.com/Watcharaphong-kob/support-ticket-triage-agent/pull/2) created and attached to this chat; tracking issue #1 closed as completed. Hosted CI **succeeded** for commit 8d50edc in [run 37904012936](https://github.com/Watcharaphong-kob/support-ticket-triage-agent/actions/runs/37904012936). Later documentation-only delivery metadata is checked locally; no code changed after the green hosted run. Final ZIP head/checksum are in the external SUBMISSION_MANIFEST.json.
