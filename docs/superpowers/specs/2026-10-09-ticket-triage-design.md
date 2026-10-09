# T01 — Support Ticket Triage Agent Design

9 October 2026 · T01 approved by the user · T02 authorized; use uv for package management

## Purpose and success criteria

Create a small homework submission demonstrating grounded triage of complete customer conversations using an OpenAI GPT model and at least two executable tools. It must process all three supplied tickets, preserve Thai text, produce understandable decisions, and include the prompt, tool definitions, README, and maximum-one-page write-up. Readability, maintainability, extensibility, and logic take priority within the recommended 150–240 minutes.

Assignment requirements come from the supplied DOCX. Language, library choices, output schema, severity rubric, and execution limits below are proposed decisions. They are not an official answer key.

## 1. Language, interface, and boundaries

Approved choice: **Python CLI**, with Python 3.11 as the minimum target, the official OpenAI Python SDK for model access, Pydantic for contracts, pytest for tests, and Ruff for linting. Use **uv** for package management, a single pyproject.toml with runtime and development dependencies, and a committed uv.lock for resolved versions.

The CLI accepts one ticket or a file of tickets and prints JSON results. The default demonstration processes all three supplied conversations. A separate trace option shows tool execution without contaminating JSON output. Proposed invocation after packaging: python -m triage_agent --input data/sample_tickets.json, with --trace as an optional flag.

Configure the key with OPENAI_API_KEY and the GPT model with OPENAI_MODEL. The model must support tool calls; verify the chosen model and SDK API during integration. Do not hard-code a model version or include a real key. Offline fake-model tests work without credentials; live execution reports a clear configuration error when credentials/model are missing.

The CLI produces triage recommendations and draft responses. No chat UI, HTTP service, database, agent framework, vector database, deployment, automatic messaging, refunds, or account mutations are in this design. A TypeScript CLI remains an alternative if that is your preferred language; this draft selects Python to keep the implementation compact.

## 2. Architecture and data flow

Ticket loader → validated conversation → prompt and tool-capable model adapter → bounded agent loop → allowlisted tool dispatcher → final result validation → policy consistency checks → JSON result and optional trace.

Use the module layout from docs/PROJECT_TASK_PLANNER.md. cli.py handles input/output; schemas.py owns contracts; agent.py owns model/tool orchestration; tools.py owns mock tools; policy.py owns action consistency and fallback. The prompt and mock fixtures remain separate files.

Each message includes its original text, sequence, and supplied relative time. Preserve provided translations separately from original Thai text, and label them as supplied translations. Never manufacture absolute timestamps from phrases such as just now. Customer IDs are synthetic fixture IDs mapped to the supplied customer metadata.

The agent sees the entire conversation and reconciles later messages with earlier ones. Tool results are returned to the model as tool results, with call IDs retained. The model adapter is replaceable with a fake for deterministic orchestration tests.

## 3. Urgency policy

Severity reflects reported impact and time sensitivity; confirmation is represented separately in rationale and uncertainties. A suspected incident may merit urgent investigation without asserting a confirmed outage. Account tier is context, not an automatic severity label.

| Urgency | Proposed rule | Example |
| --- | --- | --- |
| critical | Reported core service failure across multiple users/devices with substantial business interruption; or comparably severe ongoing harm requiring immediate human investigation | Thai Enterprise ticket with repeated error 500, affected coworkers, and imminent client demo |
| high | Material financial risk, blocked paid entitlement, or a substantial time-sensitive individual problem without evidence of broad service failure | Repeated reported charges, no Pro access, presentation in two hours, dispute threat |
| medium | Meaningful functional impairment with limited impact, no acute harm/deadline, and no broader incident evidence | Non-cosmetic feature malfunction requiring technical investigation |
| low | Cosmetic issue, how-to question, or feature request without material interruption or acute harm | Dark-mode behavior plus scheduling request |

Apply the highest supported severity among the ticket's unresolved issues. Anger alone does not make a ticket critical. Missing information must not silently downgrade a clearly reported serious problem; document the uncertainty and escalate when appropriate.

## 4. Action policy

| Primary action | Conditions | Destination |
| --- | --- | --- |
| escalate_to_human | Critical incident, financial dispute/repeated charges requiring account intervention, or inability to produce a safe supported decision after tool/model failure | incident_on_call, billing_payments, or human_support |
| route_to_specialist | Unresolved product/technical issue needing investigation, without the immediate escalation conditions above | product_support or technical_support |
| auto_respond | Retrieved knowledge directly supports a safe answer for the unresolved issue and no escalation/routing condition remains | null |

Urgency and action are separate: a low-severity bug can require a specialist. Critical results always escalate. Billing harm described in sample 1 always escalates. If a ticket combines a bug and a feature request, choose one primary action addressing the main unresolved problem and retain secondary issues.

No retrieved article means no grounded auto-response. References must point to document IDs actually returned by the knowledge-base tool. A draft acknowledgement is allowed during routing/escalation, but must not promise a resolution, refund, feature, or SLA unsupported by evidence.

## 5. Tool contracts

Both tools are read-only mock implementations. The demonstration requires successful execution of both before treating a model result as complete. If required tool evidence cannot be obtained, return an explicit fallback, not a fabricated successful triage.

| Tool | Arguments | Result |
| --- | --- | --- |
| get_customer_history | customer_id: non-empty string | status: ok/not_found/error; customer: object or null; error: string or null |
| search_knowledge_base | query: non-empty string; product, issue_type, locale: optional strings | status: ok/error; documents: list of up to five matches; error: string or null |

Customer objects contain customer_id, plan, tenure_months, region, seats, and prior_support_summary. Preserve unknown region/seats as null. Documents contain id, title, excerpt, locale, and is_mock=true. An empty document list is a valid no-match result. Use a simple deterministic term/category search for the mock KB; do not add embedding infrastructure.

The KB contains clearly labeled illustrative billing, service-access, and theme articles. It does not establish live regional status, actual refund timing, or real company feature availability. The dispatcher validates arguments and rejects unknown tool names. Customer text and retrieved content cannot override system instructions.

## 6. Output contract

All fields below are present; nullable fields use null and list fields use empty lists when no value is known. Reject unexpected fields and invalid enum values. Do not present a technical failure as a normal completed triage.

| Field | Type and meaning |
| --- | --- |
| ticket_id | Non-empty string; supplied or synthetic fixture identifier |
| status | completed or fallback |
| urgency | critical/high/medium/low; null only on a fallback when no reliable classification is available |
| product | String or null; never infer an actual product name from plan tier or export features alone |
| issue_type | Non-empty string describing the primary issue; null allowed on fallback |
| customer_sentiment | positive/neutral/frustrated/angry/mixed/unknown |
| secondary_issues | List of concise strings |
| next_action | auto_respond/route_to_specialist/escalate_to_human |
| destination | Allowed destination from the action table; null only for auto_respond |
| rationale | Non-empty explanation grounded in the conversation and tool evidence |
| draft_response | String or null; Thai for the Thai customer's draft; no invented promises |
| knowledge_sources | List of retrieved KB document IDs actually used |
| uncertainties | List of unknown or unverified facts |
| tool_calls | List of tool execution records with name, call_id, and status |
| error | null for completed; structured code/message for fallback |

A completed result requires a valid urgency, primary issue, both required tools having succeeded, and consistent action/destination fields. A fallback always escalates to human_support, records its failure cause, and preserves trustworthy available fields. It does not guess urgency to satisfy the schema.

Keep provider/tool internals and secrets out of the customer draft. Optional traces may include redacted arguments and results for debugging; full customer text is not needed in routine logs.

## 7. Limits and error handling

Proposed defaults: 30-second timeout per provider request; at most six model requests per ticket, including one possible retry for a transient provider error or invalid final output; at most eight individual tool executions. Stop with fallback when any budget is exhausted. Count parallel tool calls individually, and validate them before dispatch. Exact SDK wiring belongs to T07, while these limits are policy decisions.

Unknown tools, malformed arguments, missing customers, or KB errors return explicit errors to the agent. The agent may correct a call within the remaining budget. If no grounded decision emerges, fallback. Missing credentials stop a live batch before requests and return a clear nonzero CLI error. Other per-ticket failures produce fallback results and a nonzero batch exit code while retaining successful ticket outputs.

## 8. Sample acceptance targets

| Sample | Expected baseline | Required explanation |
| --- | --- | --- |
| 1 — Billing | high; escalate_to_human; billing_payments; angry | Three customer-reported charges, failed entitlement, two-hour deadline, dispute threat; payment settlement/refund state unverified |
| 2 — Thai access | critical; escalate_to_human; incident_on_call; frustrated | Cross-device/browser and coworker access failure, business risk, operational-status discrepancy; Asia-wide outage and all 45 users affected remain unconfirmed |
| 3 — Theme | low; route_to_specialist; product_support; mixed | Earlier advice failed; possible cosmetic theme bug plus separate scheduling feature request; actual availability unverified |

These baseline labels follow this draft rubric. A policy change requires updating the tests and reasoning targets together. Draft Thai replies must preserve uncertainty rather than turning the customer's regional hypothesis into a confirmed diagnosis.

## 9. Verification and task handoff

Test fixtures preserve all three four-message conversations. Unit checks cover both tools, empty matches, unknown customers, and validation. Fake-model integration checks exercise tool dispatch, tool results returned to the model, both-tool completion, budget exhaustion, bad citations, contradictory actions, invalid output, and injection attempts. Sample-case assertions check supported facts and decision policy, not exact wording.

Run a live GPT smoke check separately when a key and chosen model are available. State honestly whether it ran. A clean-checkout run, README, one-page write-up, and repository/ZIP checks complete the submission.

T01 status: **approved by the user**. T02 is authorized with uv as the package manager and creation of one GitHub repository. Initialize Git and commit the reviewed baseline at T02, then use the managed worktree workflow from docs/GITHUB_REPO_PLAN.md for project implementation. Repository and verification evidence will be recorded with the completed T02 task.
