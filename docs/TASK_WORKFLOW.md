# Task checking workflow

User instruction recorded 9 October 2026: use ask-matt before and after every task to select the right checking/testing flow.

## Before each task

1. Consult the installed ask-matt skill and follow its applicable route. It is a skill router, not a test runner.
2. Read the current spec, task acceptance, dependencies and existing implementation. Select only a ready task; preserve Phase 1 Docker/classic RAG scope.
3. Record the intended deliverable, test boundary and observable acceptance. Reuse established boundaries. Confirm new test boundaries as required by the selected TDD flow.
4. Reuse the isolated implementation worktree and run baseline checks with uv. Investigate failures before attributing them to new work.
5. For a new implementation plan, obtain the review required by writing-plans before executing it. Use the implementation/TDD flow for behavior changes.

## After each task

1. Consult ask-matt again and choose the closing route: implementation work closes with testing and code-review; a planning task closes with a spec/plan self-review.
2. Run relevant checks, inspect exit codes, and record actual outputs. Full implementation suites run at the end; live model/database checks are reported separately from setup checks.
3. Review implementation against standards and its task spec. Resolve actionable findings before marking the task complete. Reviewers use a recorded starting commit and a task-scoped diff.
4. Update the shared task registry, planner, TODO and HTML only when acceptance is met. Record failures/skips honestly.
5. Commit only authorized changes after verification. Respect previous declined operations; do not silently publish or push unrelated local documentation.
6. Report the deliverable, evidence, remaining limits and next ready task. Do not equate an installed dependency or a written plan with a working feature.

## Current checkpoint

- Before T03 planning: ask-matt consulted; route selected: plan review → implementation with TDD → standards/spec review.
- Existing isolated worktree: feat/triage-agent at commit 4844b1bdc4bdea9d449e983dc48efbce7e0cc884.
- Fresh baseline: uv run --locked pytest -q; 8 passed.
- After T03 planning: ask-matt consulted again; plan self-review checked source fidelity, customer context, scope and neighboring contracts. Ruff check/format passed for the generator; HTML structure, JavaScript syntax, all 35 source blocks and deterministic regeneration verified. Plan and workflow are embedded in the HTML planner view.
- Historical checkpoint: the user authorized continued implementation/testing through T05. Ask-matt was consulted before and after T03, T04, E02, E03, E04 and T05; verification and independent standards/spec review followed. The per-task tickets record steps and results. GPT-loop implementation was pending at that historical checkpoint; GitHub issue publication is separate from local ticket creation.

Skill source: C:/Users/ASUS/.codex/skills/ask-matt/SKILL.md. This workflow implements the user's instruction; ask-matt itself does not certify successful results.

## Reviewer-guide follow-up

S01 consults ask-matt before and after documentation work. Existing CLI and Docker tool/database seams are reused; no new seam or runtime change is needed. Fresh Docker suite: 65 passed/1 host-only skip. Simplicity means fewer necessary concepts and less duplication while retaining readable code, Word requirements and tested protections. S02 is a separate proposed refactor; no runtime shortening is claimed.
