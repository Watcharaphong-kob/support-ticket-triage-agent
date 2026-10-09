# GitHub Repository Plan — Support Ticket Triage Agent

Planning addition · 9 October 2026 · Complements PROJECT_TASK_PLANNER.md

Current scope: Phase 1 Docker classic RAG prototype using PostgreSQL + pgvector. GraphRAG is deferred to Phase 2. The invoked to-spec workflow published the spec/checkpoint as issue #1. Older layout and commit-group suggestions below are expanded by the current planner.

## 1. Current state and proposed repository

T02 created the private repository. Completed Phase 1 code is delivered on feat/triage-agent; docs/verification.md records review, tests and delivery evidence. [GitHub issue #1](https://github.com/Watcharaphong-kob/support-ticket-triage-agent/issues/1) tracks the spec. The main branch retains its original setup until reviewed integration; use the delivery branch or standalone source+.git ZIP. CI is configured for pushes/PRs; remote execution status is reported separately.

| Setting | Proposed choice |
| --- | --- |
| Repository name | support-ticket-triage-agent |
| Description | OpenAI GPT support-ticket triage with customer-history and knowledge-base tools, structured decisions, and Thai/English sample conversations |
| Owner | Watcharaphong-kob |
| Visibility | Private; give the evaluator access before submission |
| Default branch | main |
| Implementation branch | feat/triage-agent — completed Phase 1 delivery branch |
| Delivery | Repository URL plus reproducible README; ZIP with source and .git if GitHub submission is unavailable |

These are recommendations. The assignment specifies a repository or ZIP fallback, but not a repository name, branch strategy, visibility, CI provider, or license. Keep the original employer document local unless you intend to include it in the submission; do not add an open-source license to supplied employer material by default.

## 2. Planned repository layout

```text
support-ticket-triage-agent/
  README.md
  WRITEUP.md                     # maximum one page
  pyproject.toml                 # package, runtime, dev dependencies
  uv.lock                        # committed dependency lock
  Dockerfile                     # uv-managed Python application image
  compose.yaml                   # application + PostgreSQL/pgvector
  migrations/                    # knowledge schema and vector extension
  .env.example                   # empty/example values only
  .gitignore
  .github/
    workflows/ci.yml
  src/triage_agent/
    __init__.py
    cli.py
    schemas.py
    agent.py
    tools.py
    policy.py
    knowledge/                   # ingestion, embedding adapter, PostgreSQL search
  prompts/system.txt
  data/
    sample_tickets.json
    customers.json
    knowledge_base.json
  tests/
    test_tools.py
    test_agent.py
    test_policy.py
  examples/
    sample_results.json           # label mock versus live output
  docs/
    ASSIGNMENT_SUMMARY.md
    PROJECT_TASK_PLANNER.md
    GITHUB_REPO_PLAN.md
    ASSIGNMENT_READER.html
```

The docs/ placement is a future organization proposal. Existing planning files remain at the workspace root today. The user selected uv: use pyproject.toml and uv.lock, uv sync --locked for installation, and uv run --locked for checks. Commit the lockfile and ignore .venv/.uv-cache. Sample data will be synthetic except for the supplied assignment conversations.

Proposed ignore rules: .env, .env.* with an exception for .env.example; .venv/; __pycache__/; *.pyc; .pytest_cache/; .ruff_cache/; .coverage; htmlcov/; build/; dist/; *.egg-info/; .worktrees/; local logs and traces; submission archives. Do not ignore source, prompt files, tests, fixtures, or CI configuration. Keep real keys out of commits and history.

## 3. Repository setup sequence

1. At T02, initialize local Git on main, after the project design choices are settled.
2. Create .gitignore and include the planning documents and project metadata in an explicit initial commit. Review the staged file list; do not blindly stage the employer DOCX or local configuration.
3. Create an empty GitHub remote with the selected owner/name/visibility, then connect origin and push the baseline. Choose either local initialization plus an empty remote, or cloning a preinitialized remote; avoid creating conflicting initial histories.
4. Create or reuse an isolated implementation worktree from the committed baseline using the workflow below.
5. Complete Phase 1 tasks in dependency order, including Docker infrastructure, ingestion, classic RAG and database integration checks, with meaningful commits and recorded verification.
6. At T12, review the diff, merge the reviewed branch into main, verify a clean clone, and prepare the submission URL/archive.

Repository setup belongs inside T02 and delivery inside T12. This plan does not add another 210-minute schedule. If authentication or remote setup takes too long, continue with local Git and use the assignment's ZIP fallback.

## 4. Worktree workflow

Git worktrees allow multiple checkouts of the same repository, with separate checked-out branches. See the [official Git worktree documentation](https://git-scm.com/docs/git-worktree).

1. Inspect the Git directory, common directory, current branch, and superproject before creating anything. Reuse a suitable linked worktree when one already exists; a submodule is not evidence of isolation.
2. Commit the planning/configuration baseline first so the worktree has a known starting commit. Uncommitted files in the primary checkout are not automatically copied into a new worktree.
3. Prefer Codex's managed worktree creation and attachment tools when available. Select the committed baseline explicitly if there is no remote default branch yet. Work in the returned directory and inspect its branch state; do not assume it created the suggested branch name.
4. If managed/native tools are unavailable, use a manual worktree at .worktrees/triage-agent. Before creation, commit the .worktrees/ ignore rule and verify it with git check-ignore. The fallback directory is a proposal, not a directory created by this plan.
5. Install dependencies inside that checkout and run its baseline checks. If only documentation exists, report that no application tests exist yet; do not report a passing test suite. Once tests exist, resolve baseline failures before proceeding.
6. Make implementation commits inside the isolated checkout. In a detached managed checkout, use the app's branch/integration controls before pushing; do not assume a named branch exists.
7. After integration, preserve any needed ignored files and clean up a managed worktree using the app's archive tool. For a manual worktree, use Git's worktree removal workflow after checking for uncommitted work. Do not recursively delete a checkout to clean up Git metadata.

Keep the primary checkout on main and use one implementation branch for this short assignment. Avoid a separate develop branch or one worktree per small task. Additional branches/worktrees are useful only when there is actual independent work.

## 5. Commit and review plan

| Commit group | Planner tasks | Suggested commit message |
| --- | --- | --- |
| Baseline | T01–T02 | docs: record assignment plan and project setup |
| Contracts/data | T03–T04 | feat: add ticket fixtures and validated triage contracts |
| Docker / knowledge | E02–E04 | feat: add Docker PostgreSQL ingestion and classic RAG |
| Tools/prompt | T05–T06 | feat: add customer history and database knowledge tools |
| Agent/output | T07–T08 | feat: implement bounded GPT tool loop and action policy |
| Verification | T09–T10 | test: cover triage scenarios and failure paths |
| Submission | T11–T12 | docs: document setup evaluation and sample results |

Keep changes reviewable and truthful; commit messages describe implemented behavior, not planned behavior. A single pull request from the implementation branch to main is sufficient. Include the problem solved, tool/decision behavior, checks actually run, and any live-model verification limitation. Do not claim a successful live run based on fake-model tests.

## 6. Lightweight GitHub tracking

Publish the Phase 1 spec as a single issue with the ready-for-agent label after the to-spec test-boundary confirmation. The canonical planner tracks implementation subtasks; no extra board or milestone is required. GraphRAG remains a separate Phase 2 scope.

## 7. CI and reviewer experience

Create one lightweight workflow for pull requests and pushes to main: check out source, select the supported Python version, install declared development dependencies, run chosen lint/format checks, and run offline tests. Match the commands in CI to the README. Pin workflow action revisions when authoring the workflow. GitHub provides a [Python build-and-test guide](https://docs.github.com/en/actions/tutorials/build-and-test-code/python).

Default CI should use fake GPT and embedding adapters against real Docker PostgreSQL/pgvector, requiring no API key. Keep lightweight setup tests independent of Docker. Live GPT/embedding smoke runs are separate opt-in checks; record whether they ran. If configuring live CI later, use repository secrets and avoid passing them to untrusted pull-request code.

The README should make the reviewer path obvious: prerequisites → create environment → install → configure their own key/model → run three tickets → inspect JSON and tool traces → run offline tests. Include sample results and mark how they were generated. Ensure a private repository is accessible to the reviewer before sending its URL.

## 8. Submission checklist

- [ ] Repository owner/name/visibility selected; reviewer access verified.
- [ ] main contains the intended final implementation and all R1–R11 deliverables.
- [ ] README commands work from a clean clone in a new environment.
- [ ] Offline checks pass; live verification status stated accurately.
- [ ] Thai text and all three four-message conversations are intact.
- [ ] Prompt plus two tool schemas/implementations are easy to locate.
- [ ] WRITEUP.md is no more than one page in its intended rendering.
- [ ] Tracked files and commit history contain no actual API key or customer secrets.
- [ ] Example outputs identify mock/live provenance and do not invent verified facts.
- [ ] Submission URL references the final main commit; optionally tag that tested commit submission-v1.
- [ ] If using ZIP fallback, package the primary repository's source plus its actual .git directory, excluding virtual environments, worktrees, caches, secrets, and unrelated local files.
- [ ] ZIP fallback extracted elsewhere and checked for usable Git history and runnable source.

For the ZIP fallback, do not zip only a linked worktree: its .git is usually a pointer to shared metadata elsewhere. Package the self-contained primary repository so the reviewer receives the Git history required by the assignment.

## Delivered prototype

Reviewed code is pushed to feat/triage-agent and available in [draft PR #2](https://github.com/Watcharaphong-kob/support-ticket-triage-agent/pull/2). Tracking issue #1 is closed as completed. [GitHub Actions run 37904012936](https://github.com/Watcharaphong-kob/support-ticket-triage-agent/actions/runs/37904012936) succeeded for delivery commit 8d50edc. Main remains available for reviewed integration. Local SUBMISSION_Phase1.zip contains source and standalone .git; SUBMISSION_MANIFEST.json records its final commit and checksum.
