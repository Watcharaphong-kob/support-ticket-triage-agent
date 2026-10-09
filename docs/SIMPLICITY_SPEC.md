# Simplicity and Reviewer Acceptance Spec

## Problem Statement

The user wants the prototype's code to be as simple and short as possible, and wants clear ways to test it, judge assignment fit and let another person reproduce it from GitHub. Passing offline tests alone does not prove live GPT reasoning or semantic retrieval quality.

## Solution

Use the main Word assignment as the binding requirement. Keep the selected uv/Docker/classic-RAG architecture. Prefer direct readable code, fewer concepts and less duplication; retain necessary validation, tool execution, citations, language handling and visible failures. Provide a reviewer guide separating automated contract tests, offline sample demonstrations and live quality evaluation. Any later simplification must preserve public behavior and prove the change at the existing CLI and tool/database boundaries.

## User Stories

1. As a reviewer, I want an exact clone branch, so that I obtain the complete prototype.
2. As a reviewer, I want prerequisites stated, so that I know whether host Python is needed.
3. As a developer, I want my own local environment settings, so that credentials remain private.
4. As a reviewer, I want one full Docker test command, so that database tests are not silently omitted.
5. As a reviewer, I want expected results and skip explanations, so that I can interpret a test run.
6. As a reviewer, I want a credential-free demonstration, so that I can verify tool/database wiring.
7. As a reviewer, I want live GPT evaluation distinguished from canned output, so that confidence is honest.
8. As a reviewer, I want semantic embedding evaluation distinguished from fake vectors, so that RAG claims are supported.
9. As an operator, I want a whole-thread rubric, so that urgency reflects evolving impact.
10. As a reviewer, I want citations checked against source content, so that plausible JSON is not mistaken for grounded reasoning.
11. As a Thai customer, I want Thai source text and drafts preserved, so that language survives testing/refactoring.
12. As a reviewer, I want missing history and tool failure distinguished, so that uncertainty is disclosed.
13. As a developer, I want direct code with minimal repetition, so that a prototype remains easy to understand.
14. As a developer, I want optional demonstration content kept separate from GPT logic, so that the live path stays clear.
15. As a developer, I want existing tests reused, so that shortening code cannot silently change behavior.
16. As a reviewer, I want requirement coverage and remaining evidence gaps stated, so that I can judge submission readiness.
17. As another developer, I want fresh-clone startup steps, so that I can reproduce the project without local caches.
18. As an owner, I want private repository access explained, so that an evaluator can choose repository access or the permitted source archive.

## Implementation Decisions

- The original assignment and previously selected prototype scope take precedence over code-length goals.
- "Simple and short" means minimal necessary concepts, direct control flow, readable names and removal of repeated logic; it does not mean compressed one-liners or deletion of error checks/tests.
- Keep the current explicit OpenAI SDK tool loop and one PostgreSQL/pgvector knowledge database. No new agent framework, graph backend, generic plugin system or orchestration layer.
- Reuse the existing JSON CLI and read-only tool/database interfaces. No new public testing seam is needed; these boundaries were already approved and verified during Phase 1.
- Before a later refactor, record runtime size and duplication candidates. Evaluate moving canned offline demonstration text out of live-model logic and consolidating repeated serialization/decision construction where it reduces total complexity.
- Do not shrink code by hardcoding the supplied ticket IDs, skipping either tool, inventing citations, dropping Thai handling or masking failures.
- Preserve input/result contracts, execution budgets, safe provider errors, UTF-8 output, read-only parameterized retrieval and embedding-space validation.
- Existing demonstration and test behavior remains available. Reducing runtime lines is useful only if equivalent behavior is proven and readability improves.
- Requirement fit uses a documented human rubric and explicit confidence limits. A subjective score is not an official assignment grade.

## Testing Decisions

- Prefer highest existing boundary: JSON CLI with the deterministic model against real Docker PostgreSQL. Assert observable outputs, tool records, citations, exit codes and stderr separation.
- Reuse current tool/retrieval, provider HTTP, UTF-8 and offline-configuration tests; do not test private helpers solely because code moved.
- Preserve the three original conversations and all twelve messages. Compare urgency/action evidence, unknown facts, separate feature requests and Thai drafts.
- Require the complete Docker suite and host Compose check after runtime changes. A host test run with DB skips is insufficient.
- Demonstration tests prove plumbing and policy constraints. Separately run live GPT and live embeddings with user-owned credentials to assess actual reasoning, grounding, multilingual relevance and generalization.
- For fresh-clone acceptance, verify access/prerequisites, environment setup, startup, migration, ingestion, sample execution and test results without relying on a prior cache or database.

## Out of Scope

- New runtime functionality, production deployment or automatic customer actions.
- GraphRAG in this phase.
- Guaranteed live-model accuracy, an official employer grade or an arbitrary line-count target.
- Runtime refactoring merely because this specification was written. Refactor implementation is a separate follow-up task.

## Further Notes

Current evidence: 65 Docker tests pass with one host-only skip; the separate host Compose check and hosted CI pass. Live paid GPT/semantic embedding checks remain unperformed. Runtime size baseline is 1,054 nonblank Python lines, excluding tests, prompt, SQL and planning artifacts. Reviewer instructions and acceptance criteria are documented; no runtime shortening is claimed.

Published follow-up: [GitHub issue #3](https://github.com/Watcharaphong-kob/support-ticket-triage-agent/issues/3), ready-for-agent. S01 documentation is complete; S02 runtime simplification is still proposed.
