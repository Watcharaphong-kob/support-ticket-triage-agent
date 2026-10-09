# Assignment Summary

## What you need to build

A Support Ticket Triage Agent that uses an OpenAI GPT model to process complete customer conversations, classify urgency (critical/high/medium/low), extract product/issue type/sentiment, search a knowledge base, and choose auto-response, specialist routing, or human escalation. Use at least two executable tools; mocks are allowed.

## What you need to submit

- Working code processing the three supplied tickets.
- The system prompt and tool schemas plus implementations.
- A README explaining setup and execution.
- A write-up of at most one page covering architecture decisions, failure handling, and production evaluation.
- A GitHub repository, or a ZIP containing source and .git if you cannot push.
- Do not include an actual API key; the reviewers supply their own.

## What matters most

The recommended time is 150–240 minutes. Evaluation focuses on readability, maintainability, extensibility, and logic. A terminal console or API is enough; a chat UI is unnecessary.

Read the entire thread. Ticket 1 evolves into repeated reported charges and a deadline. Ticket 2 describes a Thai Enterprise access failure across devices and coworkers despite an operational status page. Ticket 3 combines unresolved theme behavior with a scheduling feature request.

## Recommended planning direction

Start with a Python CLI, a bounded GPT/tool loop, mocked customer-history and knowledge-base tools, structured decisions, and focused tests. This is a proposed architecture, not a language requirement. The detailed planner allocates 210 minutes and includes dependencies, acceptance checks, risks, and evaluation targets.

The document does not specify a model version, programming language, official sample labels, submission deadline, or deployment platform. Confirm those design choices before implementation. This deliverable is planning and document conversion; it does not implement or publish the project.
