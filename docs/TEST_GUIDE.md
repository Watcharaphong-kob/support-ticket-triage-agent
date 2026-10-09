# Test Guide and Assignment Fit

## 1. How to test

Use the completed branch, not the older main branch. This repository is private, so the owner must grant access before someone else can clone it. Git and Docker with Linux containers/Compose are the only host prerequisites for the Docker route; Python and uv are installed inside the image.

```powershell
git clone --branch feat/triage-agent --single-branch https://github.com/Watcharaphong-kob/support-ticket-triage-agent.git
cd support-ticket-triage-agent
Copy-Item .env.example .env
# Edit .env: replace POSTGRES_PASSWORD. Keep EMBEDDING_BACKEND=fake for offline testing.
docker compose up -d --build app
docker compose run --rm app python -m triage_agent.knowledge.manage ingest
docker compose run --rm -e TRIAGE_TEST_DATABASE=1 app python -m pytest -q -p no:cacheprovider
docker compose run --rm app python -m triage_agent --input data/sample_tickets.json --offline --trace
```

On macOS/Linux use `cp .env.example .env` instead of `Copy-Item`; Docker commands are the same. First startup needs internet access to download images/dependencies. The CLI container exits after each command; that is normal. PostgreSQL stays running. Stop it with `docker compose down`, which retains the knowledge volume.

Expected automated result: **65 passed, 1 skipped**. The skipped test needs the host Docker CLI; it is checked separately on the host and in CI. All database integration tests run inside the container using disposable schemas. A host-only `uv run --locked python -m pytest -q` may skip database tests and therefore is not a replacement for this Docker command.

The offline sample command needs no OpenAI key. Its JSON explicitly says `offline_demo` and `fake-token-v1`; it demonstrates executable tools, database retrieval and routing safeguards, not GPT intelligence or semantic retrieval accuracy.

To test actual GPT behavior, set your own `OPENAI_API_KEY` and compatible `OPENAI_MODEL` in `.env`, then omit `--offline`:

```powershell
docker compose run --rm app python -m triage_agent --input data/sample_tickets.json --trace
```

That run still uses fake vectors if your embedding configuration remains fake. For semantic RAG testing, follow README's separate live Compose project/volume instructions, choose a supported embedding model/dimension and re-ingest there. Never mix fake and live embedding spaces. Live provider requests use your account and may incur charges. No live provider tests have been performed by this implementation session.

## 2. How to tell whether it works for this task

First check structural behavior: three results, correct ticket IDs, complete ordered source threads, both actual tools recorded, valid urgency/action fields, real retrieved chunk IDs and disclosed mock provenance. Stdout must be JSON; traces belong to stderr. Exit 0 means completed triage, 1 means at least one explicit human fallback, and 2 means invalid input/configuration. A completed result means contract/policy checks passed, not that every model judgment is correct.

Then assess reasoning against the whole conversation:

| Sample | Project expectation | Evidence that should drive the decision |
| --- | --- | --- |
| Repeated reported charges and no Pro access | high; escalate_to_human; billing_payments | Three reported charges, missing access, presentation in two hours and dispute threat; settlement/refund status unverified |
| Thai Enterprise error 500 | critical; escalate_to_human; incident_on_call | Multiple devices/browsers/coworkers, major-client demo and green-status-page conflict; no confirmed Asia outage; Thai draft |
| Theme behavior and scheduling request | low; route_to_specialist; product_support | Failed System Default attempt, nonblocking theme issue and separate scheduling feature request; do not repeat failed advice |

These are this project's rubric, not an official answer key from the Word document. Unknown product should remain null; Free/Pro/Enterprise are plan names. Do not accept invented refunds, SLAs, confirmed outages or feature availability. Check that cited passages support the draft/rationale rather than merely containing similar words.

Use a fourth ticket unlike the supplied samples with the live GPT mode to check generalization. Review mixed issues, evolving urgency, missing history, empty knowledge and hostile instructions. The deterministic offline model is a limited demonstration and cannot validate general-ticket classification. Compare live outputs with a human rubric across repeated runs; record disagreements, citation errors, failure rate, latency and cost.

## 3. Does it fit the main Word assignment?

**Assessment: 8/10 for current submission readiness. This is a reasoned self-assessment, not an employer score.**

The required deliverables are present: GPT adapter and prompt, urgency/extraction/action contracts, two tool schemas and implementations, CLI processing, three faithful sample conversations, README, source/Git history and a verified one-page architecture/failure/production-evaluation write-up. Mocks are allowed by the assignment. Independent review found two CLI defects, both fixed with failing-then-passing tests; no actionable spec gaps remained. Hosted CI and clean-clone setup passed.

The remaining confidence gap is live GPT and multilingual semantic RAG quality: mocked HTTP and canned offline decisions cannot establish them. Code is also larger than the minimal Word exercise because the user selected Docker and classic RAG. Runtime currently contains **1,054 nonblank Python lines**, including management, validation, ingestion and offline demonstration code. No line-count reduction has yet been implemented. The new simplicity spec prioritizes readable, direct code and removal of duplication while retaining the original requirements and tested protections.

## 4. Can someone else clone and run it?

**Yes, if they have repository access, Git, Docker/Compose, and follow the completed branch's README.** The Docker route does not require host Python/uv. They must create their own `.env`, replace the local DB password, start the services, migrate/ingest knowledge and choose offline or live mode. Adding `.env` alone does not start the database or seed knowledge.

Compose automatically reads `.env`; direct host uv/Python commands do not. Host execution needs the documented environment variables. Do not share your `.env` or API key. A different laptop should create its own named volume; reusing an existing volume requires its existing password and compatible embedding space. Use the standalone source-plus-Git ZIP if private GitHub access cannot be arranged.
