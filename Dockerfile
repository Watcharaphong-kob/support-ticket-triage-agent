FROM python:3.12.14-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.12.6 /uv /uvx /bin/
WORKDIR /app
ENV UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=never PYTHONUNBUFFERED=1
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --locked --no-install-project
COPY src ./src
COPY data ./data
COPY prompts ./prompts
COPY tests ./tests
COPY docs/assignment_source.json ./docs/assignment_source.json
RUN uv sync --locked
ENV PATH="/app/.venv/bin:$PATH" TIKTOKEN_CACHE_DIR=/app/tokenizer-cache
RUN python -c "import tiktoken; tiktoken.get_encoding('cl100k_base')"
RUN useradd --create-home --uid 10001 appuser
USER appuser
CMD ["python", "-m", "triage_agent", "--help"]
