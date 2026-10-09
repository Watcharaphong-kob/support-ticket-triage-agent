# LangChain / LangGraph Triage Prototype Plan

Status: proposed design and delivery checklist. This commit creates the plan only; framework/API implementation has not started. Review this document before coding. Keep all planning updates in this file.

Branch: `feat/langchain-langgraph`, based on `feat/triage-agent` at `c295253`. The previous prototype remains available on its delivery branch.

## Goal and scope

Build the main Word assignment's support-ticket triage agent using LangChain and LangGraph, with the shortest readable implementation that supports both terminal and HTTP use. Preserve urgency, product/issue/sentiment extraction, whole-thread reasoning, knowledge search, two real read-only tools, next-action selection and the three original English/Thai tickets.

Required deliverables:

1. Working terminal command and HTTP API calling the same triage implementation.
2. System prompt and two tool definitions, including argument schemas and implementations.
3. README with clone/setup/ingest/run/test instructions for both entry points.
4. A verified one-page write-up covering architecture and why, failure handling, and production evaluation.
5. Tests and sample evidence that distinguish framework wiring from real GPT quality.

The original Word assignment remains the authority. Both CLI and API, the framework choice, uv and Docker classic RAG are user requirements added to that assignment. GraphRAG remains a later phase.

## Approach selection

**Recommended: LangChain `create_agent` backed by LangGraph.** LangChain supplies model/tool integration and structured output; LangGraph runs the agent graph. This uses both requested frameworks without maintaining a second hand-written model/tool loop.

Alternative: an explicit LangGraph `StateGraph` with custom model, tool and validation nodes. It provides more control but adds state, transitions and failure paths. Use it only if implementation proves that required behavior cannot be expressed clearly with `create_agent` and small middleware. Do not silently switch approaches.

Do not build two independent agents, add a multi-agent supervisor, introduce graph checkpoints, or use deprecated `create_react_agent` examples. This is stateless ticket triage, not a chat application.

## Small architecture

```text
JSON file -> CLI ----+
                    +-> triage_batch -> per-ticket LangChain agent / LangGraph
POST /triage -------+                     |-> customer-history tool
                                          |-> knowledge-search tool -> PostgreSQL
                                          +-> structured decision -> evidence/policy check
                                                                    -> JSON result or fallback
```

- Reuse the existing Pydantic ticket, tool and result contracts, prompt, customer fixtures and PostgreSQL knowledge implementation.
- Keep one batch validator and one batch triage function. CLI and API handle transport only; neither implements routing or model logic.
- Replace the custom agent loop and direct GPT adapter with `create_agent` and `ChatOpenAI` after framework-level tests establish equivalent required behavior.
- Return an internal structured decision from the model. Tool execution records, ticket identity, status and errors are application-owned; never trust the model to supply them. Final validation builds the public result from actual execution evidence.
- Prefer provider-native structured output with a compatible configured GPT model. Document the required model capabilities. If a tool-based output strategy is needed, distinguish its synthetic output tool from the two real assignment tools and include it in budget accounting.
- Keep all request state local to a ticket invocation. Customer scope, tool records and retrieved documents must never leak across API requests.
- Keep PostgreSQL/pgvector, ingestion and embeddings intact initially. No new LangChain database integration package is needed to call the existing search implementation.

### Simplicity rules

- Fewer concepts and duplicate paths matter more than raw line count. No compressed one-liners or deleted protections to meet a target.
- Add only `api.py` as a runtime file unless a concrete responsibility requires another file. Prefer modifying the existing agent, tools, schemas and CLI modules.
- Remove superseded custom-loop/provider code after the replacement passes; do not retain two production implementations on this branch.
- Remove the bulky canned production model when replaced; use injected scripted/fake chat models in tests. The framework branch's documented runtime is live GPT. Existing offline-demo behavior remains available on the original branch; README must make this intentional difference clear.
- Reuse the current prompt and package resources; do not create additional prompt copies.
- Record before/after nonblank runtime lines and actual files/concepts removed. Current baseline: 1,054 nonblank runtime Python lines and 80 tracked repository files. CLI plus API adds capability, so do not claim improvement solely from a line-count comparison.
- This planning stage adds only `plan.md`. Later planning/checklists/evidence remain in this file and README; no new planner, ticket-copy, diagram or research files.
- Existing inherited documents remain intact during this plan-only stage. During delivery, remove obsolete generated planning copies only after preserving requirements and useful evidence in the retained documents; update CI accordingly.

## Terminal and API contract

### Shared behavior

- Accept one existing `Ticket` object or a list of 1-100 tickets; reject empty batches and duplicate ticket IDs before invoking the model or tools.
- Preserve original message order, Thai characters, relative times and supplied translations.
- Return one JSON envelope containing mode, embedding model and a result per ticket, consistent across transports. Runtime mode is `live_gpt`.
- Completed results require both actual tools, valid citations and action-policy checks. Missing history is disclosed; tool failures and unverifiable decisions produce a visible human-review fallback.

### Terminal

- Retain `python -m triage_agent --input data/sample_tickets.json --trace` and the installed `triage-agent` command.
- Stdout is JSON; safe trace records go to stderr.
- Exit 0 for all completed results, 1 if any result falls back, and 2 for invalid input/configuration.

### HTTP

- Use FastAPI with one `POST /triage` endpoint accepting the shared input contract and returning the same envelope as the CLI.
- Return HTTP 422 for invalid ticket JSON, empty/oversized batches or duplicate IDs before processing. Return sanitized HTTP 503 for unavailable required runtime configuration.
- Validly accepted batches return HTTP 200 even when individual results contain fallback; clients inspect each result's status/error. Document this explicitly rather than hiding failures.
- Add `GET /health` for process liveness only; do not describe it as database/model readiness. FastAPI's existing OpenAPI/docs pages supply request documentation; no custom UI.
- Use a synchronous endpoint so blocking graph/database work executes through FastAPI's worker mechanism. Build ticket-specific execution state inside the shared function, not a global mutable trace.
- Serve locally on port 8000; Docker publishes to loopback. Auth, external hosting and deployment are outside this prototype.

## Tool definitions

Use LangChain tools with existing Pydantic argument schemas and short descriptions. Return model-visible data plus application-owned execution evidence using supported tool results/artifacts; verify the selected framework version's behavior before relying on it.

| Tool | Argument schema | Implementation | Observable outcomes |
| --- | --- | --- | --- |
| `get_customer_history` | Required nonempty `customer_id`; reject extra fields | Read synthetic customer fixtures; enforce the current ticket's customer scope | `ok`, `not_found`, or sanitized `error`; mock provenance explicit |
| `search_knowledge_base` | Required nonempty query, at most 8,000 characters; optional product, issue type and English/Thai locale filters | Existing read-only PostgreSQL exact-vector search, top five passages | `ok` with actual source/chunk IDs, excerpts and mock flags; empty success differs from failure |

Do not count structured-output helpers as either required tool. Do not add refund, account-update, shell or arbitrary-SQL tools. Each completed ticket must contain verifiable records of both real tools.

## Failure handling and policy

- Set provider timeout to 30 seconds and disable SDK retries. For this branch, prefer immediate disclosed fallback over recreating the old custom correction/retry loop; this is an intentional simplification to document and test.
- Use built-in per-run model/tool limit middleware: at most six model requests and eight tool calls. A separate graph recursion guard must be documented as a graph-step limit, not a substitute for either call budget.
- Fail closed for unknown tools, malformed arguments, foreign customer access, invalid call IDs, tool/provider errors, invalid structured output, missing required tool evidence or invented citations. Preserve pre-execution rejection of unauthorized calls; check full batches before any execution where necessary.
- Do not rely on prompt instructions alone for authorization or citation validity. Keep application checks small and concentrated in the existing tool/policy modules.
- Define routing precedence explicitly: critical impact routes to incident review; otherwise billing issues route to human billing review; otherwise apply the proposed action with existing evidence checks. This resolves the original critical-plus-billing destination conflict and needs a regression test.
- Auto-response remains draft-only, low urgency, supported by retrieved evidence and known customer history. No response is sent automatically.
- Preserve missing-history uncertainty and mock-knowledge labeling. Thai tickets require Thai drafts. Treat customer/knowledge content as untrusted data; semantic grounding still requires evaluation.
- Prevent embedding-space changes from contaminating an existing index; continue using a separate database/volume for a different model or dimension.

## Dependencies and files

Use Python 3.11+, uv, LangChain, LangGraph, `langchain-openai`, Pydantic, FastAPI and Uvicorn; reuse existing PostgreSQL/pgvector/tokenization dependencies and pytest/Ruff. Resolve compatible versions during implementation and commit the uv lockfile; do not guess pins in this plan.

Expected modifications: `pyproject.toml`, `uv.lock`, existing agent/tools/schemas/policy/CLI modules, Docker Compose, README, existing prompt where necessary, and relevant tests. Add `src/triage_agent/api.py` plus focused framework/API tests. Remove obsolete runtime code only after replacement verification.

Keep `WRITEUP.pdf` at the root; update its existing editable source rather than creating another write-up. The current documentation/reader tooling must either stay valid or be intentionally retired from this branch with CI updated; do not leave broken generation checks.

## Delivery checklist

Each task consults ask-matt before and after, uses tests at public seams, and records actual skill/plugin usage and results here. Never report a planned test as passed.

### F01 — Framework agent through the terminal

- [ ] Write failing framework-level tests: full thread reaches the model, both real tools execute, actual tool IDs/citations are retained, unauthorized customer access cannot execute.
- [ ] Run those tests and confirm meaningful failures against the current custom-loop implementation.
- [ ] Add locked framework dependencies; adapt the two tools; replace the loop with `create_agent`; preserve shared result validation and visible fallback.
- [ ] Test provider/tool failures, unknown calls, budget exhaustion, forged citations, missing history, Thai drafts and critical billing precedence.
- [ ] Demonstrate all three original tickets through the terminal using an injected scripted model against real Docker PostgreSQL. This proves framework wiring, not GPT quality.
- [ ] Run focused tests, review the diff and commit a working terminal slice. Record results here.

### F02 — HTTP access to the same agent

Blocked by F01.

- [ ] Write failing API tests for one ticket, batch input, invalid JSON/schema, empty/oversized batches, duplicate IDs, fallback output and missing configuration.
- [ ] Add the small FastAPI module and local Docker/API startup command; reuse the shared batch validator and triage function.
- [ ] Compare API and CLI envelopes for identical injected model/tool results. Test simultaneous requests to prove customer/evidence isolation.
- [ ] Verify invalid requests invoke neither model nor tools, Thai JSON survives HTTP, and health reports liveness accurately.
- [ ] Run terminal + API tests, review the diff and commit a working dual-entry-point slice. Record results here.

### F03 — Submission and quality evidence

Blocked by F02.

- [ ] Remove superseded custom-loop/canned-model code and obsolete generated planning copies only where the retained implementation/docs cover their useful behavior and evidence.
- [ ] Update README with uv/Docker setup, ingestion, terminal commands, HTTP examples, compatible GPT configuration, failures and exact tests. Adding an environment file alone is not DB startup/ingestion.
- [ ] Update the system prompt and tool definitions as delivered artifacts; verify installed prompt/migration resources and packaged entry points.
- [ ] Write and render the one-page architecture/failure/evaluation PDF; inspect layout and verify exactly one page.
- [ ] Run locked install, Ruff, package builds, complete Docker database tests, terminal and HTTP samples, and fresh-clone startup. Record test counts and before/after runtime complexity.
- [ ] With an owner-provided key, evaluate all three source tickets plus unseen billing, access and product tickets using live GPT. Evaluate live embeddings separately from fake-vector wiring. If credentials are unavailable, mark these checks unperformed and do not claim semantic quality.
- [ ] Review the entire branch against the Word requirements and this plan. Confirm reviewer access and the correct GitHub branch URL before submission.

## One-page write-up outline

Use three compact sections in the existing write-up, with no task history:

1. **Architecture and why:** shared CLI/API triage function, LangChain agent running on LangGraph, two read-only tools, structured output/evidence validation, Docker classic RAG; explain why a custom graph/checkpoint system was unnecessary.
2. **What can go wrong and handling:** ambiguous or multi-issue tickets, prompt injection, missing customer history, provider/DB failures, loops, forged/stale citations, mock evidence and embedding mismatch; bounded execution, scoped tools and disclosed fallback.
3. **Production evaluation:** labeled multilingual held-out tickets; urgency/action/product/issue/sentiment accuracy; critical-case false negatives; citation relevance/support; unsafe automation rate; latency, token cost and fallback rate; regression checks and human review before deployment.

## Acceptance and review gate

- The main Word deliverables are present, with terminal **and** API support as requested.
- Both entry points use the same agent and observable contracts; no duplicated decision logic.
- Tool definitions include schemas, descriptions and implementations; both real tools are evidenced before completion.
- Code gets simpler by removing a second implementation and repetition, not hiding complexity or dropping checks.
- Write-up is verified as one page and covers all three requested topics.
- No secrets, paid keys or unnecessary new planning files are committed.
- This plan is a proposal. Approve its architecture, API contract and intentional retry/offline/policy changes before implementation. Implementation work will use this same file for detailed steps and progress.

## Primary references checked

- [LangChain agent stack and LangGraph relationship](https://www.langchain.com/oss-overview)
- [LangChain agents](https://docs.langchain.com/oss/python/langchain/agents)
- [Structured output](https://docs.langchain.com/oss/python/langchain/structured-output)
- [Built-in model/tool limit middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in)
- [FastAPI request bodies](https://fastapi.tiangolo.com/tutorial/body/)

Skill usage for this plan: ask-matt before/after, Superpowers brainstorming, reuse of the existing isolated worktree, primary documentation verification and pre-delivery checks. No framework dependencies or runtime code were installed/changed while writing the plan.
