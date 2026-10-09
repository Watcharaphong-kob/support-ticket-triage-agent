# Project TODO — Support Ticket Triage Agent

9 October 2026 · T01/T02 done · 2 of 12 tasks complete · Next: T03

## Tech stack

Python >=3.11 (development 3.12), uv with pyproject.toml + uv.lock, OpenAI SDK 2.54.0, Pydantic 2.14.0, argparse CLI, pytest 9.1.1, Ruff 0.16.10, setuptools packaging, UTF-8 JSON fixtures, Git/private GitHub. Offline GitHub Actions checks are planned; no workflow exists yet. Dependency versions are from the current uv.lock, not a promise to use those versions forever.

Model: runner selects a tool-capable OpenAI GPT model through OPENAI_MODEL. Key: runner supplies OPENAI_API_KEY. No actual key goes into the repository. No chat UI, API service, database, or vector store is required by the approved design.

## Spec checkpoints

Agent-library, database, and retrieval design: AGENT_KNOWLEDGE_SPEC.md. Current runtime is the OpenAI SDK with an explicit loop planned. Classic RAG recommendation: PostgreSQL + pgvector. Framework alternatives: openai-agents or langgraph. GraphRAG alternative: neo4j + neo4j-graphrag. New libraries/databases are proposed, not installed.

Full spec: docs/superpowers/specs/2026-10-09-ticket-triage-design.md. Detailed tasks and requirements: PROJECT_TASK_PLANNER.md.

- [x] Python CLI and uv-managed package baseline; credential-free startup and safe configuration.
- [ ] Preserve all three full conversations, Thai text, translations, and relative times.
- [ ] Validate urgency, product/issue/sentiment, secondary issues, and all approved result fields.
- [ ] Execute both customer-history and KB tools; keep mock facts clearly labeled.
- [ ] Apply impact-based urgency and consistent auto-response/routing/escalation rules.
- [ ] Ground replies in retrieved IDs; no invented refund, outage, SLA, or feature claims.
- [ ] Generate Thai customer drafts for the Thai case.
- [ ] Enforce 30-second timeout, maximum 6 model requests and 8 tool executions per ticket.
- [ ] Make invalid output/tool failures visible; fallback escalates to human_support.
- [ ] Test offline orchestration and sample reasoning; report live-model verification separately.
- [ ] Finish README, prompt, tool definitions, one-page write-up, and clean-checkout submission checks.

## Task list

- [x] **T01 — Design:** approved Python CLI, severity/action rules, output/tool contracts, and limits.
- [x] **T02 — Setup:** uv package + lockfile, config, CLI, Git/worktree, private GitHub; 8 tests, Ruff, and builds pass.
- [ ] **T03 — Fixtures:** data/sample_tickets.json and data/customers.json; three tickets, four messages each; synthetic IDs, Thai/translations, no invented dates.
- [ ] **T04 — Contracts:** src/triage_agent/schemas.py; validated input/tool/output types, nullable unknowns, enumerations, and completed/fallback consistency.
- [ ] **T05 — Tools:** src/triage_agent/tools.py and data/knowledge_base.json; two callable tools with schemas, bounded mock search, explicit misses/errors.
- [ ] **T06 — Prompt:** prompts/system.txt; whole-thread reasoning, grounding, Thai replies, injection resistance, severity and action policy.
- [ ] **T07 — Agent:** src/triage_agent/agent.py; GPT adapter, allowlisted tool dispatch, returned tool results, environment key/model, call limits and timeout.
- [ ] **T08 — Decisions/output:** src/triage_agent/policy.py and CLI integration; consistent actions, validated citations, explicit fallback, JSON stdout and optional stderr traces.
- [ ] **T09 — Tests:** tools, fake-model loop, policies, all three scenarios, errors, budgets, invalid citations, and injection attempts; keep offline checks key-free.
- [ ] **T10 — Demo:** run three sample tickets; inspect reasoning and both tool calls; run live GPT smoke check when credentials are available and state actual verification status.
- [ ] **T11 — Docs:** complete reviewer README and maximum-one-page WRITEUP.md; architecture, implemented safeguards, production evaluation, labeled examples.
- [ ] **T12 — Submission:** clean-checkout run, checks/CI as applicable, secrets review, reviewer access, final repository commit or self-contained ZIP with .git.

## Baseline case expectations

| Ticket | Urgency | Action / destination | Key check |
| --- | --- | --- | --- |
| 1 — Charges / no Pro | high | escalate_to_human / billing_payments | Preserve deadline and reported financial harm; charges/refund state unverified |
| 2 — Thai access failure | critical | escalate_to_human / incident_on_call | Preserve coworker/browser evidence and status discrepancy; do not confirm an Asia-wide outage |
| 3 — Theme / scheduling | low | route_to_specialist / product_support | Separate possible cosmetic bug from feature request; do not invent availability |

These labels follow the approved project policy. The assignment supplies no official answer key. Track genuine implementation completion, not installed dependencies, when checking tasks off.

## Agent / database / RAG extension TODOs

These tasks are outside the original 210-minute baseline. Full interfaces, data models, and acceptance criteria are in AGENT_KNOWLEDGE_SPEC.md. Choose the backend before adding dependencies.

- [ ] E01 — Select main agent runtime and database/retrieval approach; review the architecture addendum.
- [ ] E02 — Add only selected packages with uv; configure database and migrations; commit updated uv.lock.
- [ ] E03 — Implement source/chunk IDs, idempotent ingestion, metadata, embedding model/dimensions, and versioned indexes.
- [ ] E04 — Implement classic RAG/backend-neutral search behind the existing KB tool, with explicit no-match and citations.
- [ ] E05 — If GraphRAG is selected: sourced entities/edges, bounded read-only traversal, and multi-hop test queries.
- [ ] E06 — Evaluate English/Thai retrieval, provenance, stale sources, outages, and data isolation; compare relevance, groundedness, latency, and cost.
