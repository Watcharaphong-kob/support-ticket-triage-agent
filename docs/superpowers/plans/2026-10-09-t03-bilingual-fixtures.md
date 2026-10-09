# T03 Bilingual Fixtures Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Supply faithful, reusable JSON fixtures for all three assignment tickets and their synthetic customer records.

**Architecture:** Keep source conversations separate from triage expectations. JSON files form the public input boundary; source-fidelity tests compare their contents with the frozen assignment transcription. Existing CLI processing remains pending until later tasks.

**Tech Stack:** Python 3.12, uv, standard-library JSON, pytest, Ruff. No new dependencies.

**Spec:** docs/PROJECT_SPEC.md, docs/project_tasks.json (T03), and the message-preservation/customer-history contracts in docs/superpowers/specs/2026-10-09-ticket-triage-design.md. The current Phase 1 spec supersedes the historical mock-only knowledge scope.

## Global Constraints

- All 3 tickets retain 4 messages, ordering, relative times, Thai and supplied translations; synthetic customer IDs labeled; no invented dates.
- Customer objects contain customer_id, plan, tenure_months, region, seats, and prior_support_summary. Preserve unknown region/seats as null.
- Customer IDs are synthetic fixture IDs mapped to the supplied customer metadata.
- Phase 1 is a Docker classic-RAG prototype; GraphRAG belongs to Phase 2. T03 prepares data only.
- Use uv and the existing lockfile; no API key is required for fixture verification.

## Review Focus

- Thai Unicode, punctuation and emoji must survive UTF-8 JSON loading without paraphrasing.
- Similar relative times must preserve distinct message positions; never calculate calendar timestamps.
- Supplied English translations remain separate from the original Thai text.
- Reported pending charges and regional hypotheses remain customer claims, not confirmed account/incident facts.
- Synthetic identifiers and unknown metadata are explicit; Enterprise's first critical issue must not become a claim of no previous support tickets.

## Files and public interface

- Create data/sample_tickets.json: top-level list of three ticket objects.
- Create data/customers.json: top-level list of three synthetic customer objects.
- Create data/README.md: field contract, provenance, synthetic IDs and limits.
- Create tests/test_fixtures.py: tests at the JSON-file boundary, using the existing pytest/unittest conventions.
- Add docs/assignment_source.json to the implementation worktree as the frozen reference already present in the primary checkout. Verify it against the original DOCX before relying on it.
- Update docs/project_tasks.json and rebuild the primary planner/TODO/reader only after T03 passes review.

Ticket objects contain ticket_id, customer_id, is_synthetic_id, source_sample, locale, customer_info and messages. Use ticket-001/customer-001 through ticket-003/customer-003; is_synthetic_id is true. customer_info preserves the supplied customer-info sentence verbatim without the numbered heading prefix.

Each message contains sequence (1–4), relative_time, text and supplied_translation (string for the four Thai messages; null for English). relative_time is the supplied phrase verbatim; text is the customer message without the outer quotation delimiters. No timestamps, urgency labels, action targets or invented product names are added to these inputs.

Customer objects retain the approved fields plus is_synthetic=true and source_sample (1–3). Plans are Free, Enterprise, Pro; tenure_months are 4, 8, 5. Only sample 2 has region=Thailand and seats=45; other unknown values are null. Support summaries preserve the supplied first-contact/first-critical/no-previous distinctions. Upgrade attempt and daily usage are retained through customer_info, not asserted as verified billing/telemetry records.

## Task 1: Preserve all ticket conversations

**Consumes:** The independent source transcription, paragraphs 32/33, 35/36 and 38/39.

**Produces:** UTF-8 JSON ticket list with the interface above, for T04 input validation and later CLI demonstrations.

- [x] Confirm the JSON fixture boundary and review this plan before implementation.
- [x] Consult ask-matt before implementation; reuse the existing isolated worktree. Record the starting commit and run uv run --locked pytest -q.
- [x] Write test_ticket_conversations_match_assignment: assert exactly three samples; four ordered messages each; reconstruct message/relative-time/translation source segments and compare against the independent transcription. Assert Thai originals remain in text and translations remain separate.
- [x] Run uv run --locked pytest tests/test_fixtures.py -q; expect failure because the fixture file does not exist.
- [x] Add data/sample_tickets.json with all 12 source messages and supplied customer metadata, without derived labels or dates.
- [x] Run the focused test; expect success and no missing or altered source content.

## Task 2: Link synthetic customer history safely

**Consumes:** Ticket customer IDs and supplied customer-info paragraphs.

**Produces:** Three customer records for the later get_customer_history tool, not a working tool itself.

- [x] Write test_customer_records_preserve_supplied_context: assert one unique record per ticket ID; explicit synthetic provenance; plans/tenures Free/4, Enterprise/8, Pro/5; only Enterprise Thailand/45; other region/seats null; support summaries retain the source distinctions.
- [x] Run the focused test; expect failure because customer fixtures are absent.
- [x] Add data/customers.json and data/README.md with the exact field/provenance contract. Treat all billing and outage statements as reported claims.
- [x] Run the focused fixture tests; expect success without credentials or network.

## Task 3: Verify and close T03

- [x] Consult ask-matt after implementation; follow its closing route through verification and code-review.
- [x] Run uv run --locked pytest -q, uv run --locked ruff check . and uv run --locked ruff format --check .; expect zero failures and unchanged setup behavior.
- [x] Review standards and T03 spec fidelity independently, using the recorded baseline and task-scoped diff. Check the five Review Focus cases explicitly.
- [x] Record concrete test counts and review findings in docs/T03_FIXTURE_STATUS.md; resolve findings before setting T03 done.
- [x] Update the canonical task registry, regenerate planner/TODO/HTML, and verify matching task counts and preserved source paragraphs.
- [x] Commit only the reviewed T03 implementation files if permitted; do not retry the previously declined unrelated documentation push. Report the commit/publication state honestly.

## Plan self-review

T03 acceptance maps to Tasks 1 and 2; all five Review Focus risks are covered by the source-fidelity/customer tests. JSON fields above define the boundary for T04 without prematurely implementing its Pydantic schemas. Docker provisioning and agent processing remain in their owning tasks. Source fidelity is tested against independently supplied assignment content, not a snapshot generated from the new fixtures.

Planning checkpoint: baseline 8 tests passed. The user authorized continued implementation/testing through T05. T03 source checks passed and final review was completed; see the T03 execution ticket.
