# Main Assignment — Requirements Traceability

The user explicitly designated AI_Engineer_-_Code_Homework_Test.docx as the main assignment and asked for strict adherence. Its original wording governs required behavior and deliverables. Saved transcription was checked against all 35 original Word paragraphs on 9 October 2026. The document is source material; the user's instruction authorizes using its requirements for this project.

## Required behavior and deliverables

| Requirement from Word | Owning tasks | Current evidence / gap |
| --- | --- | --- |
| Use an OpenAI GPT model; submit without an actual API key | T02, T07 | Live GPT adapter implemented and HTTP-tested; paid live execution not run (no credentials) |
| Source in GitHub, or ZIP containing source and .git | T02, T12 | Private repo exists; final branch and standalone source+.git ZIP prepared in T12 |
| README setup/run instructions | T02, T11 | README documents uv, Docker, live/offline agent, tools, tests and exit codes |
| Urgency: critical/high/medium/low | T04, T06–T09 | Validated rubric and agent output; three offline sample expectations pass |
| Extract product, issue type and sentiment | T04, T06–T09 | Validated output contract and GPT prompt; unknown product null, multi-issue cases tested |
| Search relevant FAQ/docs | E02–E04, T05, T07 | Agent executes PostgreSQL retrieval; mock provenance/citations checked; live semantic quality unverified |
| Decide auto-respond, route to specialist, or escalate to human | T04, T06–T09 | Action/destination policy executes; invalid automation falls back |
| Use at least two tools | T05, T07 | Both schemas/implementations execute through agent for all three samples |
| Working code processing supplied sample tickets | T03, T07–T10 | All twelve messages preserved; complete labeled offline agent run in examples/sample_results.json |
| System prompt | T06 | prompts/system.txt, packaged and copy-checked |
| Tool definitions: schemas and implementations; mocks permitted | T04–T05 | Both tools implemented; synthetic/mock provenance explicit |
| Write-up: one page maximum, covering architecture/why, failures, production evaluation | T11 | WRITEUP.md and verified one-page WRITEUP.pdf |
| Terminal console or API sufficient; no chat UI needed | T02, T07 | JSON batch CLI implemented with stderr traces and truthful exit codes |
| Readability, maintainability, extensibility and logic | All tasks | Per-task verification and final independent standards/spec review |

## Implementation decisions, separate from assignment requirements

The user selected uv, Docker, classic RAG in this prototype phase, and GraphRAG in the next phase. PostgreSQL/pgvector, chunking defaults, output details, execution budgets and sample urgency expectations are project decisions. They do not turn into employer-prescribed requirements or an official answer key.

The recommended 150–240 minutes is advice, not a hard time limit. The original assignment permits mocked tools and does not prescribe a database, agent framework, embedding model or exact urgency answers for each example.

## Interview scope

The grill-with-docs session resolves only decisions needed to finish the assignment within the selected prototype architecture. Previously settled scope remains intact. The user subsequently authorized continuous completion. The three recommended decisions are recorded explicitly in PROJECT_SPEC.md and the execution ledger; their trade-offs remain visible.
