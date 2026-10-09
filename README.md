# Support Ticket Triage Agent

AI Engineer homework: an OpenAI GPT agent for support-ticket urgency, extraction, knowledge retrieval, and routing, including Thai and English conversations.

## Current status

T01 design is approved. T02 provides the package, CLI entry point, environment configuration, tests, and uv-managed dependencies. Ticket fixtures, tools, prompts, and live triage are scheduled for T03–T08 and are not implemented yet. Providing --input currently prints an explicit unfinished-processing error and exits with code 2.

## Setup

Prerequisites: Git, uv, and Python 3.11 or later. The development default in .python-version is 3.12.

```powershell
git clone https://github.com/Watcharaphong-kob/support-ticket-triage-agent.git
cd support-ticket-triage-agent
uv sync --locked
uv run --locked triage-agent --help
uv run --locked python -m triage_agent --version
```

uv manages the local .venv. Commit pyproject.toml and uv.lock; do not commit the environment. For a supported locally installed Python version, use uv sync --locked --python 3.11 (or another supported version).

## Configuration

Help, version, and offline tests need no API key. Later live execution will require both OPENAI_API_KEY and OPENAI_MODEL, supplied by the runner. .env.example contains empty example values. Copying it to .env does not automatically load it; set variables in your shell. A real key must never be committed.

```powershell
$env:OPENAI_API_KEY = "your-own-key"
$env:OPENAI_MODEL = "your-selected-tool-capable-gpt-model"
```

On macOS/Linux, use export OPENAI_API_KEY and export OPENAI_MODEL. The config object hides the key from its repr and reports missing variable names without printing their values. No default model version is assumed.

## Verification

```powershell
uv run --locked pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
uv build
```

Current tests cover credential-free startup, help/version, explicit unfinished processing, blank/missing configuration, and key redaction. They do not verify ticket triage or live OpenAI calls. Build outputs go to the ignored dist/ directory.

Use uv add for runtime dependencies and uv add --dev for development tools. Commit the resulting pyproject.toml and uv.lock changes together. The [uv project guide](https://docs.astral.sh/uv/guides/projects/) explains locking and environment management.

## Planning documents

- PROJECT_TASK_PLANNER.md — tasks and acceptance criteria.
- GITHUB_REPO_PLAN.md — branches, worktrees, CI, submission.
- docs/superpowers/specs/2026-10-09-ticket-triage-design.md — approved design.
- ASSIGNMENT_READER.html — readable source and planning documents; opens offline.

The original DOCX stays local and is excluded from Git. The planning reader includes its textual transcription. The repository is private; give the evaluator access before submission. No actual API key is included.
