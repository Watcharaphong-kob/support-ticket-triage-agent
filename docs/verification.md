# Phase 1 verification — 9 October 2026

Authority: original Word assignment, with user-selected Docker/classic-RAG prototype scope. GraphRAG remains deferred.

- Rebuilt Docker image without source mounts: **63 passed, 1 skipped**. The skipped test needs the host Docker CLI; it is verified separately on the host.
- Agent/model/policy/CLI focused suite: **27 passed**. Ruff check and formatting pass.
- Real PostgreSQL/pgvector ingestion and all three sample triage runs succeed. `examples/sample_results.json` is explicitly `offline_demo` with `fake-token-v1` embeddings. This is not a live GPT result or a model-quality benchmark.
- Sample 1: high → billing_payments; sample 2: critical → incident_on_call, Thai draft; sample 3: low → product_support, with scheduling request retained. These are project policy expectations, not an official assignment answer key.
- Both tools execute for each sample. Citations refer to actual returned chunk IDs; mock provenance and unresolved facts remain visible.
- OpenAI GPT and embedding adapters are exercised with mocked HTTP. **Paid/live GPT and semantic embedding checks were not run:** no API key/model was configured. README provides the exact opt-in commands.
- Fresh standards/spec review, clean-checkout build/tests, package-resource check, HTML checks, GitHub delivery and final commit evidence are added below as executed.

Test schemas are disposable; demonstration data remains in the public schema. Local .env, virtual environments, caches and private credentials are excluded from delivery. Actual provider exception content and tool arguments are omitted from traces.
