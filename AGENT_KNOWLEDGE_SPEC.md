# Agent, Database, RAG and GraphRAG — Design Options

9 October 2026 · Proposed extension for review · No new libraries or databases installed

## Recommendation

Keep the approved homework baseline: Python + uv + OpenAI SDK + Pydantic + two read-only tools. For a real knowledge system, start with **classic RAG using PostgreSQL + pgvector**. Consider **Neo4j GraphRAG** when questions require relationships across products, features, regions, and incidents. Choose the retrieval backend before implementation; the original T01–T12 plan remains the approved 210-minute baseline.

Framework, database, and retrieval are separate decisions. An agent framework manages execution; a database stores facts; RAG retrieves supporting content. A workflow drawn as a graph is not itself GraphRAG.

## 1. Main agent library

| Option | Python package | What it does | Fit for this project |
| --- | --- | --- | --- |
| Current approved choice | openai | Model client; application owns tool dispatch, validation, limits, and state | Recommended for the small homework; installed at T02 |
| OpenAI Agents SDK | openai-agents | Agent runtime for tools, turns, guardrails, and orchestration | First framework alternative if you want the runtime to manage the loop; proposed, not installed |
| LangGraph | langgraph | Stateful workflow orchestration with explicit control flow | Consider for durable multi-step workflows or human review/resume; proposed, not installed |

OpenAI documents the SDK as an application-side runtime that runs the loop and invokes application tools. See [OpenAI Agents SDK guidance](https://developers.openai.com/api/docs/guides/agents/sdk). LangGraph provides stateful agent orchestration; see [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview).

Choose one main orchestrator. Keep customer-history and knowledge-search implementations behind their existing tool contracts so the agent framework can change without replacing the data layer. Preserve the approved 30-second timeout, six-model-request budget, eight-tool-execution budget, output contract, and failure policy with any framework.

The installed openai package is the model SDK. openai-agents is a separate proposed dependency, not already part of uv.lock. Versions for new packages must be resolved together with the existing stack when a path is selected.

## 2. Database choices

| Option | Library / service | Store | Retrieval role | Status |
| --- | --- | --- | --- | --- |
| Homework fixtures | UTF-8 JSON | Sample customers, conversations, mock FAQ/docs | Deterministic mock search | Approved baseline; fixture/tool work pending |
| Small local persistence | Python sqlite3 + SQLite | Customers, tickets, results, document metadata | Storage; semantic vector search needs a separate design | Optional; no extra Python package for sqlite3 |
| Recommended classic RAG | PostgreSQL + pgvector; psycopg and pgvector Python integration | Business records, documents/chunks, embeddings | Vector similarity plus optional keyword search | Proposed; not provisioned or installed |
| GraphRAG | Neo4j; neo4j driver + neo4j-graphrag | Entities, relationships, chunks, embeddings, evidence | Vector/text retrieval followed by bounded graph traversal | Proposed; not provisioned or installed |

Python's [sqlite3 documentation](https://docs.python.org/3/library/sqlite3.html) describes its SQLite interface. [pgvector](https://github.com/pgvector/pgvector) adds vector similarity search to PostgreSQL and supports combining it with PostgreSQL full-text search. [Neo4j's retrieval guide](https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_rag.html) describes vector, hybrid, and Cypher-augmented retrievers.

Use PostgreSQL as the transactional store if selecting the classic-RAG path. A Neo4j path can retain JSON customer mocks for the homework, or use a separate transactional database later; do not add two databases without a concrete need. Keep customer history separate from the shared knowledge corpus.

## 3. Classic RAG spec — recommended extension

**Flow:** FAQ/docs → clean and split → embed → index chunks → ticket query → retrieve relevant chunks → agent tool result → grounded draft and triage.

Proposed components:

- **Ingestion:** Import UTF-8 articles with source ID, title, language, product/issue metadata, source version, and mock/verified flag. Start with synthetic English and Thai test content. Stable article/chunk IDs and content hashes make re-ingestion idempotent.
- **Chunking:** Preserve section boundaries and source links. Initial trial: 400–600 tokens per chunk with approximately 60 tokens of overlap; tune using retrieval tests, not assumptions. Use a tokenizer compatible with the selected embedding model.
- **Embedding:** Select a multilingual-capable embedding model and configure it separately from the GPT model. Record model, output dimension, and index version; changing the embedding space requires re-embedding and rebuilding its compatible index.
- **Storage:** documents(id, title, locale, source, version, content_hash, is_mock); chunks(id, document_id, text, metadata, embedding, embedding_model, index_version). Keep customer/ticket/result tables separate.
- **Retrieval:** Start with top_k=5, metadata filters, and exact vector similarity for a small corpus. Add keyword/vector fusion only if evaluation shows a benefit. Validate Thai queries explicitly; English tokenization/stemming does not establish Thai retrieval quality.
- **Tool output:** Preserve existing document id/title/excerpt/locale/is_mock fields. If adding chunk IDs, scores, or source versions, revise the tool schema and tests together. Scores are ranking signals, not confidence that a statement is true.
- **Generation:** Pass retrieved evidence through search_knowledge_base. Require returned document IDs in knowledge_sources. No useful match means explicit uncertainty and appropriate routing/escalation, never invented policy.

Proposed files: src/triage_agent/knowledge/{base.py,json_store.py,postgres_store.py,ingest.py}; migrations/; tests/test_retrieval.py; data/knowledge_base.json. Add only files needed by the selected backend. Agent code calls a backend-neutral search interface; it does not construct arbitrary SQL.

OpenAI's [retrieval guide](https://developers.openai.com/api/docs/guides/retrieval) explains semantic retrieval and embeddings. The PostgreSQL design here is our proposal; it is not an instruction to use OpenAI-hosted vector stores.

## 4. GraphRAG spec — alternative extension

**Flow:** FAQ/docs → chunks + sourced entities/edges → Neo4j graph and indexes → vector/keyword seed retrieval → bounded relationship traversal → cited context → agent result.

Use Neo4j's HybridCypherRetriever or VectorCypherRetriever when graph relationships add evidence. HybridRetriever alone combines vector/text search; graph expansion requires a traversal stage. The [Neo4j retrieval guide](https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_rag.html) distinguishes these retrievers.

Proposed graph model:

- Nodes: Article, Chunk, Product, Feature, IssueType, Region, Incident.
- Edges: Article HAS_CHUNK Chunk; Chunk MENTIONS entity; Article ADDRESSES IssueType; Feature BELONGS_TO Product; sourced Incident AFFECTS Product/Region.
- Every factual edge carries source_document_id, source_chunk_id, source_version, and verification/mock status. Unconfirmed customer suspicions must not become verified incident edges.
- Start with manually curated synthetic relationships, then evaluate model-based entity/edge extraction separately. Retain original chunks as the evidence; graph summaries do not replace citations.
- Trial retrieval bounds: five seed chunks and at most two graph hops. Cap returned context and deduplicate citations; evaluate whether expansion improves relevant evidence over classic RAG.
- Run allowlisted parameterized read-only traversal queries. A model-generated arbitrary Cypher query is outside this design.

Microsoft's [GraphRAG project](https://microsoft.github.io/graphrag/) is another graph-based knowledge approach. It is a separate indexing/query pipeline; it is not the Neo4j library and is not required for this homework. Compare it only if corpus-level graph summaries become a concrete requirement.

Good trial query: find documented issues for a product in a region and trace which articles/incident evidence support the answer. The supplied Thai ticket alone cannot prove an Asia-wide incident; GraphRAG must preserve that uncertainty too.

## 5. Decision and acceptance criteria

| Criterion | Classic RAG | GraphRAG |
| --- | --- | --- |
| Main evidence | Relevant document passages | Passages plus sourced relationships |
| Starting corpus | FAQ/how-to/policy documents | Corpus with useful product/feature/region/incident links |
| Extra work | Chunking, embeddings, vector index, retrieval evaluation | Classic retrieval concerns plus graph schema, entity linking, edge provenance, traversal evaluation |
| Default recommendation | Start here for this project | Adopt when relationship tests show measurable benefit |

Acceptance: source/chunk IDs resolve; re-ingestion is idempotent; no cross-customer history leakage; no-match is explicit; English/Thai retrieval tests pass; outdated source versions are identifiable; citations only use retrieved evidence; database outage follows the approved fallback. Measure retrieval recall@5, answer groundedness, routing accuracy, latency, and indexing/query cost. Compare both approaches on the same queries rather than assuming a graph is better.

## 6. Extension TODOs — outside the original time estimate

- [ ] E01 — Choose main agent runtime and JSON/SQLite/PostgreSQL/Neo4j backend; update and review the architecture addendum before coding.
- [ ] E02 — Add selected dependencies with uv and commit uv.lock; document local database configuration and migrations using synthetic data.
- [ ] E03 — Implement stable article/chunk ingestion and idempotent updates; configure embedding model/dimension/index version if using semantic retrieval.
- [ ] E04 — Implement selected RAG search backend behind search_knowledge_base; retain the JSON mock adapter for offline tests.
- [ ] E05 — If GraphRAG is selected, add sourced graph nodes/edges, bounded read-only traversals, and relationship-specific evaluation queries.
- [ ] E06 — Run bilingual retrieval, no-match, stale-source, outage, provenance, and isolation tests; compare baseline versus retrieval extension; document cost/latency and exact verification status.

These are planning tasks, not installed capabilities or an approved change to the T01 baseline. Re-estimate extension work after backend selection; it is not included in the 210 minutes for T01–T12.
