# GitHub Repository Plan — Support Ticket Triage Agent

Planning addition · 9 October 2026 · Complements PROJECT_TASK_PLANNER.md

## 1. Current state and proposed repository

The workspace at D:\Documents\OOCA_Assignment contains the assignment and planning files. Git inspection confirms it is not currently a repository, and no managed worktree is attached to this chat. Repository initialization, remote creation, pushes, issues, and worktrees have not been performed.

| Setting | Proposed choice |
| --- | --- |
| Repository name | support-ticket-triage-agent |
| Description | OpenAI GPT support-ticket triage with customer-history and knowledge-base tools, structured decisions, and Thai/English sample conversations |
| Owner | Your GitHub account or chosen organization; resolve when creating the remote |
| Visibility | Private during development; give the evaluator access before submission, or choose public if appropriate |
| Default branch | main |
| Implementation branch | feat/triage-agent — suggested name, not an existing branch |
| Delivery | Repository URL plus reproducible README; ZIP with source and .git if GitHub submission is unavailable |

These are recommendations. The assignment specifies a repository or ZIP fallback, but not a repository name, branch strategy, visibility, CI provider, or license. Keep the original employer document local unless you intend to include it in the submission; do not add an open-source license to supplied employer material by default.

## 2. Planned repository layout

```text
support-ticket-triage-agent/
  README.md
  WRITEUP.md                     # maximum one page
  pyproject.toml                 # package, runtime, dev dependencies
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

The docs/ placement is a future organization proposal. Existing planning files remain at the workspace root today. Use one dependency-management approach and record exact dependency versions or a reproducible lock/constraints file. Sample data is synthetic except for the supplied assignment conversations.

Proposed ignore rules: .env, .env.* with an exception for .env.example; .venv/; __pycache__/; *.pyc; .pytest_cache/; .ruff_cache/; .coverage; htmlcov/; build/; dist/; *.egg-info/; .worktrees/; local logs and traces; submission archives. Do not ignore source, prompt files, tests, fixtures, or CI configuration. Keep real keys out of commits and history.

## 3. Repository setup sequence

1. At T02, initialize local Git on main, after the project design choices are settled.
2. Create .gitignore and include the planning documents and project metadata in an explicit initial commit. Review the staged file list; do not blindly stage the employer DOCX or local configuration.
3. Create an empty GitHub remote with the selected owner/name/visibility, then connect origin and push the baseline. Choose either local initialization plus an empty remote, or cloning a preinitialized remote; avoid creating conflicting initial histories.
4. Create or reuse an isolated implementation worktree from the committed baseline using the workflow below.
5. Complete T03–T11 in the implementation branch with meaningful commits and recorded verification.
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
| Tools/prompt | T05–T06 | feat: add mock tools and triage system prompt |
| Agent/output | T07–T08 | feat: implement bounded GPT tool loop and action policy |
| Verification | T09–T10 | test: cover triage scenarios and failure paths |
| Submission | T11–T12 | docs: document setup evaluation and sample results |

Keep changes reviewable and truthful; commit messages describe implemented behavior, not planned behavior. A single pull request from the implementation branch to main is sufficient. Include the problem solved, tool/decision behavior, checks actually run, and any live-model verification limitation. Do not claim a successful live run based on fake-model tests.

## 6. Lightweight GitHub tracking

Optional: use one milestone, Homework submission, and six issues matching the commit groups above. Issue acceptance criteria should link to T01–T12 and R1–R11 in the planner. A small board can use To do, In progress, Review, Done. Do not create this tracking overhead if the local checklist is sufficient for the time budget.

## 7. CI and reviewer experience

Create one lightweight workflow for pull requests and pushes to main: check out source, select the supported Python version, install declared development dependencies, run chosen lint/format checks, and run offline tests. Match the commands in CI to the README. Pin workflow action revisions when authoring the workflow. GitHub provides a [Python build-and-test guide](https://docs.github.com/en/actions/tutorials/build-and-test-code/python).

Default CI should use the fake-model adapter and mocked tools, requiring no API key. A live GPT smoke run is a separate local or explicitly triggered check; record whether it was run. If configuring a live CI run later, use a repository secret rather than a tracked file and avoid passing it to untrusted pull-request code. Requiring a paid live-model check for every pull request is unnecessary for this homework.

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
