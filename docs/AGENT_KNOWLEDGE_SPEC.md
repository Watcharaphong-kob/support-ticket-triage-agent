# Agent and Knowledge System — Phase 1

9 October 2026 · Selected architecture · Phase 1 prototype implemented

## Phase decision

The user selected **classic RAG using Docker for this prototype phase**. Phase 1 uses PostgreSQL with pgvector as its sole knowledge database. GraphRAG belongs to Phase 2; its backend and libraries will be evaluated then. The existing OpenAI SDK and application-owned tool loop remain the agent approach.

The [current project spec](PROJECT_SPEC.md) defines acceptance. [Task planner](PROJECT_TASK_PLANNER.md) and [TODO](TODO.md) include Docker and classic RAG as Phase 1 work.

## Agent library and data boundaries

- Agent: installed openai SDK, Pydantic output/tool validation, explicit bounded tool dispatch. No additional agent framework is selected.
- Customer history: synthetic JSON fixtures behind get_customer_history; never mixed into the shared knowledge corpus.
- Knowledge: PostgreSQL + pgvector behind search_knowledge_base. psycopg and pgvector Python integration are installed through uv and tested against Docker PostgreSQL.
- Runtime: Docker Compose database and Python application services. Host uv commands remain available for development.
- Limits: 30-second provider timeout, at most six model requests and eight tool executions; safe human escalation on failure.

## Docker contract

Pin compatible PostgreSQL/pgvector and Python images by version or digest during implementation. Resolve Python dependencies with uv.lock. A database health check must pass before migrations and ingestion run; a running container alone does not establish database readiness. Persist knowledge in a named volume and expose development ports only on loopback. Keep credentials in runtime configuration with placeholders in examples. Destructive volume reset requires an explicit action.

See [Compose startup order](https://docs.docker.com/compose/how-tos/startup-order/) and [pgvector installation and Docker support](https://github.com/pgvector/pgvector).

## Classic RAG flow

FAQ/docs → normalize and split → embeddings → PostgreSQL chunks → ticket query embedding → top-five vector retrieval → cited tool evidence → triage and draft.

1. Ingest synthetic English and Thai articles with stable source IDs, title, language, product/issue metadata, version, content hash and mock flag.
2. Keep stable chunk IDs and parent-source relationships. Re-ingestion updates existing records without duplicates; changed or removed chunks must not leave stale evidence.
3. Start with approximately 400–600 tokens per chunk and 60-token overlap; preserve sections and tune against retrieval examples.
4. Configure the embedding model separately from GPT. Record model, dimension and index version; reject incompatible query vectors. Changing embedding space requires a compatible rebuild.
5. Use parameterized, read-only exact vector similarity queries for the small prototype corpus, top_k=5 and validated metadata filters. Scores describe ranking, not factual confidence.
6. Return document/chunk IDs, excerpts, language, version and mock provenance. Final knowledge_sources must reference returned evidence. A database failure must be distinct from a successful empty search.
7. Empty or insufficient evidence leads to uncertainty and appropriate routing; never fabricate product policy or confirmation of billing/incident facts.

## Verified test boundaries

Prefer externally visible behavior: run CLI triage with a fake GPT adapter against real Docker PostgreSQL/pgvector, and test the knowledge-search contract for ingestion, filtering, citations, bilingual data, empty results and outages. Deterministic fake embeddings test database contracts; they do not establish live multilingual semantic quality. Keep optional live embedding/GPT smoke checks separate. Existing CLI/configuration tests remain the starting point.

The user authorized continued implementation/testing through T05. The JSON fixture, schema, ingestion, retrieval and tool boundaries are verified. Full GPT CLI execution belongs to later tasks; local execution tickets record current evidence.

## Phase 2 — GraphRAG

Deferred task E05 evaluates whether sourced relationships improve retrieval over the Phase 1 baseline. Decide the graph backend then; no Neo4j, graph extraction, traversal or GraphRAG dependencies are included in Phase 1. Keep the knowledge-tool interface stable enough to compare future retrieval implementations without replacing triage policy.

## Prototype limits

No production deployment, real customer data, billing mutation, high availability, multi-tenant authentication or mandatory vector ANN indexes. No SQLite or second database. Compose, migrations, ingestion, retrieval and both tools are verified with fake embeddings; the GPT agent and live semantic quality remain pending.
