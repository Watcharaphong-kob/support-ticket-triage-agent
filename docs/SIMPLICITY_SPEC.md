# Prototype Simplicity, Repository Layout and Reviewer Acceptance Spec

## Problem Statement

The user wants the prototype's code to be as simple and short as possible, and wants clear ways to test it, judge assignment fit and let another person reproduce it from GitHub. The owner also wants fewer duplicate files and a clear repository layout. Passing offline tests alone does not prove live GPT reasoning or semantic retrieval quality.

## Solution

Use the main Word assignment as the binding requirement. Keep the selected uv/Docker/classic-RAG architecture. Prefer direct readable code, fewer concepts and less duplication; retain necessary validation, tool execution, citations, language handling and visible failures. Provide a reviewer guide separating automated contract tests, offline sample demonstrations and live quality evaluation. Maintain one consolidated local ticket record, a shared task registry and the existing GitHub tracker. Keep supporting documents together and the assignment reader easy to open. Any later simplification must preserve public behavior and prove the change at the existing CLI and tool/database boundaries.

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

19. As a developer, I want supporting documents grouped together, so that the repository root is easy to scan.
20. As an owner, I want duplicate generated ticket files removed, so that fewer copies can drift apart.
21. As an agent, I want one task registry and consolidated ticket record, so that acceptance and evidence remain available after cleanup.
22. As a reviewer, I want working document links after moves, so that instructions remain usable.
23. As an owner, I want the HTML reader at its familiar location, so that existing access still works.
24. As an owner, I want original Word content and local environment settings preserved, so that cleanup cannot erase requirements or credentials.
25. As a developer, I want disposable caches separated from source, so that cleanup cannot damage runtime or Git history.
26. As an agent, I want tool-specific validation knowledge concentrated, so that tool changes require fewer coordinated edits.
27. As an operator, I want failure timing and error codes preserved, so that refactoring does not change observable triage behavior.
28. As a developer, I want offline scenario repetition reduced only when useful, so that a cosmetic file move is not counted as simplification.
29. As a reviewer, I want completed cleanup distinguished from pending runtime work, so that ticket status reflects evidence.
30. As an owner, I want a refreshed source-plus-Git archive, so that local submission matches the cleaned repository.

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

- Supporting Markdown documents are grouped in the documentation directory; the main README, assignment reader, submission PDF and runtime configuration remain easy to locate at the root.
- Individual generated ticket copies are removed. The consolidated record retains all acceptance criteria, dependencies, skill/plugin usage, performed steps and evidence; the shared registry drives regeneration.
- The existing GitHub tracker remains authoritative for published refactor tickets. The two accepted slices are independent and both rely only on the completed reviewer guide.
- Tool-validation work concentrates tool-specific knowledge while the agent retains model turns, call IDs, budgets, transcript bookkeeping and fallback. Preserve malformed-call rejection separately from recorded argument-schema failures.
- Offline-demo work must reduce repeated construction or concepts. Moving prose or files alone is insufficient; preserve the existing model interface and both adapters.
- Remove only verified disposable/generated content during cleanup. Preserve the original assignment, local secrets, runtime, tests, active checkout and recoverable Git history.

## Testing Decisions

- Prefer highest existing boundary: JSON CLI with the deterministic model against real Docker PostgreSQL. Assert observable outputs, tool records, citations, exit codes and stderr separation.
- Reuse current tool/retrieval, provider HTTP, UTF-8 and offline-configuration tests; do not test private helpers solely because code moved.
- Preserve the three original conversations and all twelve messages. Compare urgency/action evidence, unknown facts, separate feature requests and Thai drafts.
- Require the complete Docker suite and host Compose check after runtime changes. A host test run with DB skips is insufficient.
- Demonstration tests prove plumbing and policy constraints. Separately run live GPT and live embeddings with user-owned credentials to assess actual reasoning, grounding, multilingual relevance and generalization.
- For fresh-clone acceptance, verify access/prerequisites, environment setup, startup, migration, ingestion, sample execution and test results without relying on a prior cache or database.

- Reuse the approved highest runtime seam: batch JSON CLI against real Docker PostgreSQL. No new public seam is selected by this specification.
- Repository-layout acceptance uses deterministic document regeneration, original-Word transcription comparison, relative document/reader links and consolidated-ticket coverage. These supplement runtime checks without coupling tests to private helpers.
- Existing scripted-model and tool tests protect call authorization, unknown names, duplicate IDs, batch behavior, argument failures and execution budgets. Preserve current error codes and failure timing.
- After package/resource changes, verify wheel contents and installed execution. Refresh and verify the standalone source-plus-Git archive without secrets or caches.

## Out of Scope

- New runtime functionality, production deployment or automatic customer actions.
- GraphRAG in this phase.
- Guaranteed live-model accuracy, an official employer grade or an arbitrary line-count target.
- Runtime refactoring merely because this specification was written. The approved implementation tickets remain separate, pending work.
- Broad module merging, cosmetic Python-line reduction through external data, or deletion of required validation/tests to meet a size target.

## Further Notes

Completed: Phase 1 prototype, S01 reviewer guide and S04 repository cleanup. Cleanup reduced tracked files from 101 to 80, moved eleven supporting documents, consolidated twenty-one duplicate local ticket files and removed ten disposable cache directories. Twenty-two task records remain in the consolidated planner/ticket data; fewer files does not mean fewer recorded tasks.

Pending and accepted: [S02: concentrate tool validation](https://github.com/Watcharaphong-kob/support-ticket-triage-agent/issues/4) and [S03: simplify offline demonstration](https://github.com/Watcharaphong-kob/support-ticket-triage-agent/issues/5). Both are ready-for-agent and native sub-issues of [specification issue #3](https://github.com/Watcharaphong-kob/support-ticket-triage-agent/issues/3). Neither blocks the other. Runtime simplification has not been implemented.

Latest cleanup evidence: rebuilt Docker suite 65 passed with one host-only skip; separate host Compose check passed; wheel/sdist builds, Ruff lint/format, original-Word fidelity, document links and deterministic reader generation passed. The cleaned repository and refreshed standalone submission archive preserve the original assignment and environment settings. Runtime baseline remains 1,054 nonblank Python lines, excluding tests, prompt, SQL and planning artifacts.

Live GPT and semantic embedding quality checks remain unperformed. Hosted CI passed for earlier delivery commits; the latest cleanup CI was not queried. The existing JSON CLI and read-only tool/database testing seams were approved earlier and reused for cleanup; no new seam or additional interview is needed for this synthesis.
