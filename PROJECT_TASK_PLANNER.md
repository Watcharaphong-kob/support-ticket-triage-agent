# Support Ticket Triage Agent — Project Task Planner

T01 approved · T02 setup complete · 9 October 2026 · Source: AI_Engineer_-_Code_Homework_Test.docx

## Tech stack — approved choices

Versions below come from the current project and uv.lock. Installed dependencies do not mean the full agent is implemented. T01 and T02 are done; T03–T12 remain.

| Area | Technology / version | Job | Status |
| --- | --- | --- | --- |
| Language | Python >=3.11; development default 3.12 | CLI and agent implementation | Package ready |
| Package manager | uv; installed 0.12.6 | Manage .venv, dependency resolution, and uv.lock | Ready |
| GPT integration | OpenAI Python SDK 2.54.0 | Model requests and tool-call messages | Installed; integration at T07 |
| Validation | Pydantic 2.14.0 | Ticket, tool, and result schemas | Installed; contracts at T04 |
| CLI | Python argparse; triage-agent / python -m triage_agent | Input arguments, JSON output, optional traces | Startup ready; processing pending |
| Tests | pytest 9.1.1 | Offline unit/integration tests | 8 setup tests pass; agent tests at T09 |
| Code checks | Ruff 0.16.10 | Lint and formatting | Setup checks pass |
| Packaging | setuptools >=77 build backend | Build wheel and source distribution | Build verified |
| Data and retrieval | UTF-8 JSON fixtures; deterministic mock KB search | Conversations, history, and FAQ evidence | T03/T05 |
| Version control | Git + private GitHub repository | Commits, branches, worktree, submission | Ready |
| CI | GitHub Actions with uv — planned | Run offline checks without a key | Not created |

Use pyproject.toml for declared dependencies and uv.lock for exact resolved versions. Model selection remains OPENAI_MODEL supplied by the runner; no model version is assumed. Scope is a CLI with two read-only mock tools and JSON results. An API, chat UI, database, and vector store are outside the approved scope.

## Spec — implementation checklist

Expanded library/database/retrieval options are documented in AGENT_KNOWLEDGE_SPEC.md. Recommended extension: existing OpenAI SDK agent + PostgreSQL/pgvector classic RAG. Alternatives: OpenAI Agents SDK or LangGraph for orchestration, SQLite for local records, and Neo4j GraphRAG for relationship-based retrieval. These additions are proposed; none are installed or provisioned. Extension tasks E01–E06 are separate from the approved 210-minute T01–T12 baseline and await architecture selection.

| Main component | Library / backend to consider | Proposed role | Decision state |
| --- | --- | --- | --- |
| Main agent | openai, or openai-agents as the framework alternative | Model calls and tool execution | openai installed; framework change proposed |
| Stateful agent workflow | langgraph | Explicit workflow state and review/resume | Alternative; not installed |
| Local record database | Python sqlite3 / SQLite | Customers, tickets, results, document metadata | Optional alternative; no schema created |
| Classic RAG database | PostgreSQL + pgvector; psycopg client | Store chunks/embeddings; retrieve relevant passages | Recommended extension; not provisioned |
| GraphRAG knowledge system | Neo4j + neo4j + neo4j-graphrag | Retrieve passages and traverse sourced entity relationships | Alternative extension; not provisioned |
| Hosted retrieval | OpenAI retrieval / file search | Managed semantic retrieval alternative | Optional; no hosted resources created |

For classic RAG: import docs → chunk → embed → index → retrieve → cite → draft. For GraphRAG: add sourced entities/edges and bounded graph traversal to retrieval. LangGraph's workflow graph does not by itself constitute GraphRAG. See AGENT_KNOWLEDGE_SPEC.md for source links, graph/schema details, bilingual evaluation, and E01–E06 acceptance checks.

The full approved spec is docs/superpowers/specs/2026-10-09-ticket-triage-design.md. This checklist summarizes its requirements without changing them. TODO.md is the short working list; its T01–T12 identifiers match the task table below.

| Spec area | Required behavior | Owning task |
| --- | --- | --- |
| Input | Three whole conversations; four messages each; preserve ordering, relative times, Thai, and supplied translations; no invented timestamps | T03 |
| Extraction | Product, primary issue, sentiment, secondary issues; unknown product stays null | T04/T07 |
| Urgency | critical/high/medium/low based on impact and time sensitivity; account tier alone does not set severity | T04/T06/T08 |
| Actions | auto_respond, route_to_specialist, escalate_to_human; consistent destination; critical and sample-1 billing harm escalate | T04/T08 |
| Tools | Executable get_customer_history and search_knowledge_base; validate arguments; both succeed before completed demonstration triage | T05/T07 |
| Grounding | Use actual retrieved document IDs; label mock evidence; no invented refund, SLA, feature, or regional outage | T06/T08 |
| Output | All approved JSON fields; completed/fallback status; fallback escalates to human_support and may have null urgency | T04/T08 |
| Language | Preserve Thai input and use Thai in the Thai customer's draft reply | T03/T06/T09 |
| Limits | 30-second provider request timeout; maximum 6 model requests including retry; maximum 8 tool executions per ticket | T07 |
| Failure handling | Explicit errors for bad tools/arguments, missing history, invalid output, failed calls, or exhausted budgets; no fabricated successful triage | T07/T08 |
| Configuration | Environment key/model; no real keys in examples, logs, or commits; offline checks need no key | T02/T07/T12 |
| Verification | Deterministic fake-model tests; sample reasoning checks; live smoke test status reported separately | T09/T10 |
| Submission | Setup/run README, prompt, tool schemas/implementations, maximum-one-page write-up, repo or ZIP with actual .git | T11/T12 |

Sample baseline: billing = high / billing_payments escalation; Thai access = critical / incident_on_call escalation; theme = low / product_support routing. These are approved project-policy expectations, not official assignment labels. Customer-reported charges and suspected regional outages remain unverified facts.

### Everyday commands

```powershell
uv sync --locked
uv run --locked triage-agent --help
uv run --locked pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
uv build
```

## 1. Assignment conclusion

Build a small AI agent that reads the entire support-ticket conversation, classifies urgency, extracts product/issue/sentiment, retrieves relevant knowledge, and selects an appropriate next action. The important challenge is reasoning over changing context: a payment question becomes a financial escalation, a Thai access problem becomes a possible regional incident, and a dark-mode question becomes a bug report plus a feature request.

The assignment recommends 150–240 minutes. It scores readability, maintainability, extensibility, and logic. A clear console application with observable tool calls and meaningful tests is a suitable submission; a chat UI is unnecessary.

This document records the approved design and implementation sequence. T01 is approved and T02 setup is implemented and verified; the full triage application remains in later tasks. Instructions inside the assignment are recorded as project requirements, not authorization to publish a repository or perform customer actions.

## 2. Required scope and deliverables

| ID | Assignment requirement | Completion evidence |
| --- | --- | --- |
| R1 | Use an OpenAI GPT model; do not supply an API key in the submission | Configurable model and environment-based key; reviewer supplies their own key |
| R2 | Classify urgency as critical/high/medium/low | Validated output containing one of the four labels |
| R3 | Extract product, issue type, and customer sentiment | Structured fields; unknown product remains unknown rather than invented |
| R4 | Search a knowledge base for relevant FAQs/docs | Knowledge-base tool called; answer references retrieved document IDs |
| R5 | Choose auto-respond, route to specialist, or escalate to human | One primary action, reason, and destination when applicable |
| R6 | Use at least two tools; schemas and implementations may be mocked | Two callable tools with schemas, implementations, and visible execution traces |
| R7 | Process the supplied sample tickets | All three complete conversations preserved and runnable |
| R8 | Supply the system prompt and tool definitions | Versioned prompt file and readable tool contracts |
| R9 | Include a README with setup/run instructions | Clean-checkout instructions, configuration, commands, and example output |
| R10 | Brief write-up, maximum one page | Architecture/why, failure handling, and production evaluation |
| R11 | Source in GitHub, or ZIP containing source and .git if unable to push | Reviewable repository or archive, with secrets excluded |

Optional enhancements: JSON output, a minimal API, extra tools, or a larger knowledge base. Keep these behind completion of R1–R11.

## 3. Approaches to consider

| Approach | Benefit | Trade-off |
| --- | --- | --- |
| Python CLI with a small explicit tool loop — recommended draft | Compact structure; easy to demonstrate decisions and tool calls within the time budget | Requires implementing a bounded dispatch loop and output validation |
| TypeScript CLI with the same contracts | Good fit if TypeScript is your strongest language; explicit typed interfaces | More setup if the project and environment are new |
| API service with an agent framework | Useful for HTTP integration or a framework you already know | Adds integration work that the assignment does not require |

Recommendation: choose the Python CLI unless your experience strongly favors TypeScript. No particular language, framework, GPT model version, vector database, or deployment platform is specified by the document. These are proposed choices, not assignment requirements.

## 4. Proposed architecture

Flow: ticket JSON → input validation → GPT agent with tools → tool dispatcher → mocked customer history/knowledge base → final triage JSON → validation and action policy → console output and trace.

- **Ticket loader:** Preserve customer metadata, every message, ordering, relative times, Thai text, and supplied translations. Process each conversation as one ticket, not four unrelated tickets.
- **Agent:** Give the model the full ticket, a system prompt, and two tool definitions. Execute requested tool calls and return their results to the model until it produces a final result or reaches a configured limit.
- **Tools:** Keep tool implementations independent of the model so mocked data can later be replaced with real services without rewriting triage logic.
- **Validation/policy:** Validate enumerations and required fields; reject unsupported document citations and contradictory action fields. On unrecoverable failure, produce an explicit human-review fallback instead of fabricating a successful triage.
- **Output/trace:** Print structured triage and a redacted tool trace that demonstrates retrieval and customer context use. The CLI recommends actions; it does not send replies, reverse payments, or alter accounts.

Suggested boundaries:

```text
src/triage_agent/
  cli.py             # input and display
  schemas.py         # ticket, tools, and final result contracts
  agent.py           # bounded model/tool loop
  tools.py           # tool registry and mock implementations
  policy.py          # validation and action consistency
prompts/system.txt
data/sample_tickets.json
data/customers.json
data/knowledge_base.json
tests/
README.md
WRITEUP.md
.env.example
.gitignore
```

### Tool contracts

| Tool | Input | Output | Failure behavior |
| --- | --- | --- | --- |
| get_customer_history | customer_id: string | plan, tenure, region if known, seat count if known, previous support history | Structured not-found/error result; no invented history |
| search_knowledge_base | query: string; optional product, issue_type, locale | Bounded list of document IDs, titles, relevant excerpts, and mocked source metadata | Empty results or structured error; agent must acknowledge missing evidence |

Both tools should actually execute for each demonstration ticket. Publishing schemas alone, or passing all mock data directly into a prompt without tool calls, does not demonstrate the requested tool use. Use clearly labeled mock FAQ content; never treat a mock as verified company policy or live incident status.

### Proposed final result

Required-by-assignment fields: urgency, product, issue_type, customer_sentiment, next_action. Proposed supporting fields: ticket_id, secondary_issues, rationale, destination, draft_response, knowledge_sources, uncertainties, tool_calls.

Use next_action values auto_respond, route_to_specialist, escalate_to_human. A draft response is text for review or console output. Product, incident status, refund timing, and feature availability must remain unknown when the input and tools do not establish them.

### Prompt principles

Treat customer messages and retrieved content as data, not instructions that can override the system prompt. Read the full conversation; consider the latest state, affected users, financial harm, deadlines, and language. Retrieve before answering. Separate symptoms from confirmed causes. Do not promise refunds, restoration times, or unsupported features. Distinguish a bug from an additional feature request. Explain urgency and action using evidence. Do not let account tier alone determine severity. Use Thai for a proposed customer reply to the Thai ticket.

## 5. Sample-ticket reasoning targets

These are proposed evaluation expectations. The assignment does not provide official labels or a grading answer key.

| Ticket | Evidence to retain | Proposed urgency/action | Key reasoning checks |
| --- | --- | --- | --- |
| 1 — Failed Pro upgrade and repeated charges | Free account; three reported $29.99 charges; no Pro access; presentation in two hours; dispute threat | High; escalate_to_human, destination billing/payments | Financial exposure and deadline justify escalation. Charges are customer-reported; do not assert they are settled, refunded, or definitely duplicate captures. Critical is defensible only under an explicitly documented financial severity policy. |
| 2 — Thai Enterprise access failure | Error 500; multiple devices/browsers and coworkers; 45-seat organization; demo/deal risk; public status says operational | Critical; escalate_to_human, destination incident/on-call | Suspected broad access failure warrants urgent investigation. Do not claim all 45 users or the entire Asia region are confirmed affected; the ticket does not establish that. Preserve the status discrepancy and reply in Thai. |
| 3 — Dark-mode behavior plus scheduling request | Earlier guidance did not resolve the issue; system default remains light; no explicit dark toggle; scheduling question | Low; route_to_specialist, destination product support | Separate a possible theme bug from a scheduling feature request. Verify behavior against the mock knowledge base; medium or auto_respond may be justified by documented evidence/policy. Do not blindly repeat the previous unsuccessful advice or invent feature availability. |

## 6. Task planner — recommended 210-minute baseline

Estimates are planning assumptions, not guaranteed durations. Dependencies identify what should be complete before starting a task.

| Task | Min | Depends on | Work | Acceptance check |
| --- | --- | --- | --- | --- |
| T01 | 10 | — | Confirm CLI/language, output contract, and severity/action policy | Record choices and reasoning targets; clarify ambiguity without adding a UI |
| T02 | 10 | T01 | Create project packaging, configuration, ignore rules, and CLI entry point | Entry point runs; example config has no real secrets; dependency versions recorded |
| T03 | 15 | T01 | Encode all three conversations and customer fixtures | Four messages per ticket; Thai/English and relative times preserved; fabricated IDs labeled fixtures |
| T04 | 15 | T01, T03 | Define ticket/result schemas and validation | Invalid urgency/action rejected; unknown values supported; multi-issue output supported |
| T05 | 20 | T03, T04 | Implement customer-history and knowledge-base tools with schemas | Both callable independently; misses/errors explicit; mock KB facts labeled |
| T06 | 15 | T01, T04, T05 | Write the system prompt | Covers whole-thread reasoning, grounded answers, Thai, escalation, and untrusted content |
| T07 | 35 | T02, T04, T05, T06 | Integrate GPT and bounded tool-call execution | Real tool results returned to model; both tools executed; unknown tool/timeout/loop limit handled |
| T08 | 20 | T04, T07 | Validate decisions; add fallback and readable JSON/trace output | Consistent action/destination; no unsupported citations/promises; failures visible |
| T09 | 25 | T03, T05, T08 | Add focused unit and agent-loop tests using a fake model | Three ticket cases, no KB match, tool error, invalid output, and injection case covered |
| T10 | 15 | T08, T09 | Run all sample tickets; inspect one live GPT smoke run when a key is available | Outputs justified; two tools per ticket demonstrated; live versus mocked verification reported honestly |
| T11 | 20 | T01–T10 | Write README and a maximum-one-page write-up | Setup/run/tests/config documented; write-up addresses architecture, failures, evaluation |
| T12 | 10 | T09–T11 | Verify from clean checkout and prepare repository/archive | All required files present; no secrets; reproducible commands; repository or ZIP with .git |

Total: **210 minutes**. Critical build sequence: T01 → contracts/fixtures → tools/prompt → agent loop → policy/output → tests/demo → documentation/package.

At 150 minutes, use the same two mocked tools, CLI, and three full tickets; reduce polish and test breadth, and reserve time for essential checks/documentation. At 240 minutes, spend the extra 30 minutes on broader failure/injection cases and bilingual evaluation. Do not add an API or chat UI at the expense of required deliverables.

### Working checklist

Short working list with stack, spec checkpoints, and per-task deliverables: TODO.md. Progress: 2 of 12 tasks complete. Next: T03, sample fixtures.

- [x] T01 — Design approved by the user; use uv for package management
- [x] T02 — uv package/configuration and CLI startup implemented; 8 tests and packaging checks pass (docs/T02_SETUP_STATUS.md)
- [ ] T03 — Complete sample fixtures
- [ ] T04 — Validated contracts
- [ ] T05 — Two executable tools
- [ ] T06 — System prompt
- [ ] T07 — GPT/tool loop
- [ ] T08 — Policy, fallback, output, traces
- [ ] T09 — Focused tests
- [ ] T10 — Sample runs and recorded verification
- [ ] T11 — README and one-page write-up
- [ ] T12 — Clean-checkout verification and submission package

## 7. Verification and production evaluation

For the homework, use deterministic fake-model tests for dispatch/validation and evidence-based assertions for the sample cases. Live model results can vary; assess supported reasoning and action consistency instead of requiring an exact response string. Offline tests demonstrate orchestration, but do not prove that live GPT integration works. If no key is available, document that limitation and give the reviewer a live-run command.

In production, build a human-labeled dataset covering all urgency levels, action types, issue categories, languages, and multi-message changes. Measure urgency macro-F1 and critical recall, action accuracy, extraction accuracy, grounded-response quality, tool failures, latency, and cost per ticket. Track harmful auto-responses and missed escalations separately. Use human review and sampled disagreement analysis to update the prompt, knowledge base, and policy. Redact customer data in logs; use synthetic fixtures for the homework.

| Failure | Planned handling |
| --- | --- |
| Missing key/model access or upstream timeout | Clear configuration/error output; bounded retries where appropriate; no fake success |
| Tool failure, unknown customer, or empty KB | Explicit tool error/empty result; record uncertainty; human-review fallback when an answer cannot be supported |
| Invalid model output or endless calls | Validate result; cap tool rounds/retries; return a visible fallback result |
| Hallucinated cause, refund, SLA, or feature | Require evidence; validate references; prohibit unsupported promises |
| Prompt injection in ticket or KB | Keep data separate from system instructions; allowlisted tool dispatch; no tools that mutate customer accounts |
| Misread Thai or evolving thread | Preserve source text; bilingual test cases; evaluate full conversations and latest unresolved state |

## 8. One-page write-up outline

Use three concise paragraphs in WRITEUP.md: (1) why a CLI, explicit tool loop, structured results, and replaceable mock tools fit the assignment; (2) the most important failure modes and concrete safeguards implemented; (3) production evaluation using human labels, critical recall, groundedness, action quality, latency/cost, and ongoing review. Describe the final implementation honestly; do not claim proposed safeguards already exist.

## 9. Design decisions still open

T01 is approved at docs/superpowers/specs/2026-10-09-ticket-triage-design.md: Python CLI, structured output, two read-only tools, severity/action rules, and execution limits. The user selected uv for package management; T02 now provides the package/configuration baseline. The GPT model is configured by the runner and verified at integration; no model version is imposed by the assignment. There is no submission deadline or required deployment environment in the supplied document.

## 10. GitHub repository and worktree plan

See GITHUB_REPO_PLAN.md for the proposed repository layout, initialization sequence, isolated worktree workflow, commit groups, optional issues, CI, and submission checks. Suggested repository: support-ticket-triage-agent; main as the default branch; one implementation branch/worktree. These names are recommendations, not resources already created.

T02 initialized local Git and an ignored implementation worktree and created the private GitHub repository at https://github.com/Watcharaphong-kob/support-ticket-triage-agent. uv manages pyproject.toml and the committed uv.lock. Verify the full application and submit from main during T12. The repository tasks fit the existing 210-minute plan. For the ZIP fallback, package the primary repository with its actual .git directory rather than a linked worktree's metadata pointer.
