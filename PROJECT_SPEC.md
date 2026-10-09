# Phase 1 Spec — Docker Classic RAG Prototype

9 October 2026 · User-selected phase scope · Continuous Phase 1 completion authorized

The original AI_Engineer_-_Code_Homework_Test.docx is the main assignment, as explicitly directed by the user. Follow its requirements strictly; the architecture and policy choices here implement those requirements and are not an official assignment answer key. See docs/ASSIGNMENT_REQUIREMENTS.md for required-versus-selected traceability.

## Problem Statement

The user needs a demonstrable support-ticket triage prototype that reads whole conversations, retrieves supporting knowledge, and makes justified urgency/routing decisions. Earlier planning offered several database and retrieval options without selecting one, leaving the next implementation steps unclear.

## Solution

Build Phase 1 as a local Docker Compose prototype using PostgreSQL with pgvector for classic RAG. Retain Python, uv, Pydantic, the installed OpenAI SDK, and an explicit bounded agent loop. A customer-history tool reads synthetic fixtures; a knowledge-search tool retrieves relevant document passages from PostgreSQL. Demonstrate the three supplied English/Thai conversations with JSON decisions and source citations.

Compose runs one PostgreSQL/pgvector database and a Python application service used for migrations, ingestion, samples, and tests. Host uv commands remain available for development. Database-dependent work waits for health and schema initialization. See [Docker's health-based startup guidance](https://docs.docker.com/compose/how-tos/startup-order/) and [pgvector's official documentation](https://github.com/pgvector/pgvector).

This phase is a prototype. GraphRAG is deferred to Phase 2 and is not a current dependency or service.

## User Stories

1. As a developer, I want one Compose environment, so that another machine can reproduce the prototype.
2. As a developer, I want database readiness checked, so that the application does not race initialization.
3. As a developer, I want repeatable migrations, so that local databases reach the required schema safely.
4. As a developer, I want uv-locked dependencies inside the image, so that host/container environments agree.
5. As a reviewer, I want start/stop/ingest/test/sample commands, so that I can evaluate the prototype.
6. As a reviewer, I want to supply my own key and models, so that credentials stay out of the submission.
7. As a reviewer, I want credential-free help/offline checks, so that setup is independently verifiable.
8. As an operator, I want all ticket messages read together, so that later impact changes the decision.
9. As an operator, I want impact-based urgency, so that account tier or anger alone does not determine severity.
10. As an operator, I want product/issue/sentiment and secondary issues extracted, so that mixed requests remain visible.
11. As a Thai customer, I want Thai source text preserved and a Thai draft, so that my issue is understood in context.
12. As an operator, I want supplied customer history looked up, so that account context informs triage.
13. As a knowledge maintainer, I want English/Thai articles imported, so that both languages can retrieve evidence.
14. As a maintainer, I want stable document/chunk identifiers, so that re-ingestion does not duplicate knowledge.
15. As a maintainer, I want source/embedding versions retained, so that stale or incompatible evidence is detectable.
16. As an operator, I want semantic passage retrieval, so that relevant knowledge supports the answer.
17. As an operator, I want optional product/issue/locale filters, so that results target applicable documents.
18. As a reviewer, I want source identifiers and excerpts, so that I can trace answers to evidence.
19. As an operator, I want empty search handled explicitly, so that missing knowledge does not become invented policy.
20. As a billing customer, I want repeated reported charges escalated, so that the prototype does not promise an unsupported refund.
21. As an enterprise customer, I want reported multi-user access failure escalated, so that a green status page does not dismiss my issue.
22. As a product reviewer, I want a theme bug separated from a feature request, so that failed advice is not blindly repeated.
23. As an operator, I want one action/destination, so that auto-response, routing, and escalation remain clear.
24. As a developer, I want database/model/tool failures visible, so that failure does not appear as completed triage.
25. As a developer, I want bounded calls/timeouts, so that the prototype cannot loop indefinitely.
26. As a reviewer, I want fake-model/embedding tests against real Docker PostgreSQL, so that database behavior is verified without paid requests.
27. As a reviewer, I want live verification reported separately, so that offline tests are not mistaken for live integration.
28. As a developer, I want one database for this phase, so that GraphRAG infrastructure stays in the next phase.
29. As a future developer, I want a stable knowledge-search boundary, so that Phase 2 can compare graph retrieval against this baseline.
30. As a reviewer, I want the prompt, tools, README, compact write-up and source, so that all homework deliverables remain complete.

## Implementation Decisions

- **Phase and runtime:** Docker classic RAG now, GraphRAG later. Keep the OpenAI SDK explicit loop; no framework migration is selected. Earlier database alternatives are superseded for this phase.
- **Containers:** PostgreSQL/pgvector plus Python CLI application under Compose. Pin a compatible image version/digest during setup and install application dependencies from uv's committed lockfile. Persist local knowledge in a named volume; destructive reset is separate and explicit.
- **Readiness/configuration:** Require database health and migration completion before ingestion/search. Any published database port binds to loopback. Secrets come from environment variables and are not committed. A running container alone is not readiness.
- **Data boundaries:** PostgreSQL stores knowledge documents/chunks and ingestion/embedding metadata. Customer history stays in synthetic fixtures. Mock FAQ evidence does not establish actual company policy or live incident status.
- **Ingestion interface:** Input articles carry source ID, title, content, locale, product/issue metadata, version and mock flag. Output chunks retain stable IDs, source references, text, sequence, hashes and embedding metadata. Unchanged re-imports are idempotent; changed sources replace/deactivate stale chunks without silently mixing versions.
- **Chunking:** Trial defaults are approximately 400–600 tokens with about 60 tokens overlap and preserved section/source boundaries. Tune using bilingual retrieval evidence.
- **Embeddings:** Configure model and dimension separately from GPT. Ingest/query embeddings must share compatible model/version/dimensions. Reject mismatches; changing embedding space requires an intentional rebuild. Deterministic fake embeddings are test data, not proof of semantic quality.
- **Schema:** Documents retain identity, title, source/version, locale, metadata, hash and mock status. Chunks reference documents and retain text, sequence, embedding, model/dimension, index version and hash. Enforce referential integrity and uniqueness for repeatable imports.
- **Retrieval interface:** Exact vector similarity over a small corpus, maximum five chunks, explicit metadata filters, parameterized read-only queries. Return tool-compatible IDs/titles/excerpts/locale/mock status and resolvable provenance. Ranking scores are not factual confidence. No arbitrary model-written SQL.
- **Two tools:** Customer-history lookup reads fixtures; knowledge search reads Docker PostgreSQL/pgvector. Both must execute before completed triage; history not_found permits disclosed uncertainty, while actual tool errors require fallback. Empty search is valid but does not justify a fabricated auto-response; database failure is an error, not no-match.
- **Policies:** Billing sample is high with billing escalation; Thai access failure is critical with incident escalation; theme behavior is low with product-support routing. These are project expectations, not an official assignment answer key. Preserve unknown financial state and unconfirmed regional hypotheses.
- **Result interface:** Keep ticket ID, completed/fallback status, urgency, product, primary issue, sentiment, secondary issues, action/destination, rationale, draft, retrieved source IDs, uncertainties, tool records and structured error. Unknown product remains null. Technical fallback escalates to human support; unknown fallback urgency may be null.
- **Limits:** Provider timeout 30 seconds; maximum six model requests including one possible retry, and eight tool executions per ticket. Exhaustion produces fallback. Database connection/query timeouts must also be bounded; choose and record concrete values during infrastructure implementation.
- **Language/grounding:** Preserve all four messages per sample, original Thai, supplied translations and relative times. Thai customer drafts use Thai. Cite only returned source IDs. Never invent refunds, SLA, features, settled charges or confirmed regional incidents.
- **Delivery:** JSON stdout, optional stderr traces, uv/Compose README, prompt/tool definitions, three sample runs, truthful verification, maximum-one-page architecture/failure/evaluation write-up, and repository or self-contained Git archive. No UI or deployment requirement.

## Testing Decisions

- Proposed highest seam: end-to-end CLI with a fake GPT adapter against real Docker PostgreSQL/pgvector. Assert observable results, exit status, routing, source citations and explicit failure behavior rather than private helpers.
- Second seam: the existing knowledge-search tool contract with ingestion setup. Verify idempotency, filters, bilingual source handling, top-five bounds, empty matches, citations, source changes and database outage. Keep SQL internals replaceable.
- Existing CLI/configuration tests are prior art for credential-independent startup, safe errors and stdout/stderr separation. Extend those contracts rather than adding test-only application interfaces.
- Use isolated temporary databases/fixtures and deterministic embeddings for repeatable integration checks. Cover schema initialization, references, changed sources, embedding model/dimension mismatch and query failures.
- Fake-model cases exercise all three tickets, both required tools, invalid output/citations, budgets, injection attempts and action/destination consistency.
- Fake embeddings prove storage/retrieval contracts, not multilingual semantic quality. Separately evaluate live embeddings against labeled English/Thai queries when credentials are available.
- Live GPT and embedding checks are opt-in and reported independently; offline checks require no real key. Document skipped live checks and reviewer commands honestly.
- The user authorized continuous completion. All agent/CLI/database boundaries receive offline tests and the final standards/spec review.

## Out of Scope

- GraphRAG, Neo4j, entity/edge extraction, graph traversal and graph community summaries in Phase 1.
- SQLite, a second vector database, or migration to a different agent framework.
- Production rollout, Kubernetes, high availability, production auth/tenancy, real customer ingestion, billing changes, or automatic sending/refunds.
- Chat UI, API service, unrestricted SQL and extra orchestration/infrastructure without a prototype need.
- Mandatory hybrid search/reranking or advanced ANN tuning before the small-corpus classic RAG path works.

## Further Notes

The Phase 1 implementation includes the bilingual prompt, bounded GPT adapter/tool loop, JSON CLI, database retrieval, policy and failure-path tests. Live GPT and semantic embedding quality remain unverified because no credentials were configured. The earlier 210-minute estimate covered the smaller homework baseline; Docker/database/embedding work expands scope and needs a revised estimate.

GraphRAG remains a separate Phase 2 spec and evaluation against the Phase 1 baseline. The tracking spec is published as [GitHub issue #1](https://github.com/Watcharaphong-kob/support-ticket-triage-agent/issues/1) with implementation evidence recorded in local tickets and docs/verification.md.

Selected interview decisions: search across languages by default; missing customer history permits conversation-only triage with disclosed uncertainty; mock FAQ evidence may support low-urgency demonstration auto-response drafts clearly labeled as synthetic, never actual sending. These are project decisions, not original Word requirements.
- **Simplicity:** Keep code as simple and short as possible while preserving main-assignment behavior and selected Docker/classic-RAG scope. Prefer direct readable code and less duplication; do not compress logic into unreadable one-liners or remove necessary validation/tests. The follow-up simplicity spec records acceptance; no runtime refactor is claimed.
