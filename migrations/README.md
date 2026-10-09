# Migrations

Canonical migration SQL ships with triage_agent.knowledge under migrations/.
Run python -m triage_agent.knowledge.manage migrate through uv or Compose.
The initial migration is repeatable, creates pgvector, and preserves existing records.
