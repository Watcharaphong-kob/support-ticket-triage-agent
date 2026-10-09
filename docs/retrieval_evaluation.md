# Phase 1 retrieval evaluation

Tests use real PostgreSQL 17 with pgvector 0.8.7 in Docker and a unique disposable schema. Fake lexical vectors exercise plumbing; these results do not measure multilingual semantic relevance.

Covered: bilingual excerpts/provenance; top-five bounds; read-only parameterized locale/product/issue filters; empty results; source replacement and version retention; stable IDs and repeat ingestion; embedding dimension/model space rejection; database outage; token limits and section boundaries. The complete agent/CLI tests also verify that each original sample cites a chunk belonging to its relevant billing/access/theme article. Citation validation rejects fabricated chunk IDs.

Cross-language retrieval is allowed by omitting locale. A locale filter remains an explicit optional tool parameter. Thai customer drafts remain Thai independently of retrieved document language. Fake vectors cannot demonstrate semantic cross-language matching.

For a production evaluation, curate labeled English and Thai queries with relevant source/chunk IDs (including mixed-language and no-answer queries). Evaluate recall@5, MRR, source/version accuracy, unsupported-answer rate and latency using live embeddings in a separate database space. Tune the 0.2 cosine cutoff on held-out queries; similarity is not factual confidence. Compare GraphRAG only in Phase 2 against this measured classic-RAG baseline.

Live embedding evaluation: **not run**, because no credentials were configured. See README for opt-in setup; never mix fake and live vectors in one database space.
