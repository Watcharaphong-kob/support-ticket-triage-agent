"""Explicit fake versus live embedding adapters; never silently substitute either."""

import hashlib
import math
import os
import re
from typing import Protocol

import tiktoken
from openai import OpenAI, OpenAIError

from triage_agent.knowledge.database import KnowledgeError


class Embedder(Protocol):
    model: str
    dimension: int
    index_version: str

    def embed(self, texts: list[str]) -> list[list[float]]: ...


def validate_vectors(vectors: list[list[float]], count: int, dimension: int):
    if len(vectors) != count:
        raise KnowledgeError("Embedding response count mismatch")
    for vector in vectors:
        if len(vector) != dimension or not all(math.isfinite(v) for v in vector):
            raise KnowledgeError("Invalid embedding dimension or values")
        if not any(vector):
            raise KnowledgeError("Zero embedding is not searchable")


class FakeEmbedder:
    """Deterministic lexical hash vectors for tests; not multilingual semantic embeddings."""

    model = "fake-token-v1"
    index_version = "1"

    def __init__(self, dimension: int = 64):
        if not 1 <= dimension <= 3072:
            raise KnowledgeError("Embedding dimension must be between 1 and 3072")
        self.dimension = dimension

    def embed(self, texts: list[str]) -> list[list[float]]:
        result = []
        for text in texts:
            terms = re.findall(r"[a-z0-9]+|[\u0e00-\u0e7f]", text.lower())
            if not terms:
                # Non-word content remains deterministic, including emoji-only text.
                terms = list(text)
            vector = [0.0] * self.dimension
            for term in terms:
                digest = hashlib.sha256(term.encode()).digest()
                vector[int.from_bytes(digest[:4], "big") % self.dimension] += 1.0
            norm = math.sqrt(sum(v * v for v in vector))
            result.append([v / norm for v in vector] if norm else vector)
        validate_vectors(result, len(texts), self.dimension)
        return result


class OpenAIEmbedder:
    index_version = "1"

    def __init__(self, model: str, dimension: int, *, api_key: str):
        if not model.strip() or not api_key.strip() or not 1 <= dimension <= 3072:
            raise KnowledgeError("Live embeddings require model, dimension and API key")
        self.model, self.dimension = model, dimension
        self.client = OpenAI(api_key=api_key, timeout=30.0, max_retries=0)

    def embed(self, texts: list[str]) -> list[list[float]]:
        vectors = []
        encoding = tiktoken.get_encoding("cl100k_base")
        if any(
            not text.strip() or len(encoding.encode(text, disallowed_special=())) > 8192
            for text in texts
        ):
            raise KnowledgeError("Embedding input exceeds token limit or is empty")
        try:
            # Bounded batches stay below the API's aggregate token limits for 500-token chunks.
            for start in range(0, len(texts), 32):
                batch = texts[start : start + 32]
                response = self.client.embeddings.create(
                    model=self.model,
                    dimensions=self.dimension,
                    input=batch,
                    encoding_format="float",
                )
                ordered = sorted(response.data, key=lambda item: item.index)
                if [item.index for item in ordered] != list(range(len(batch))):
                    raise KnowledgeError("Embedding response indices mismatch")
                vectors.extend(item.embedding for item in ordered)
        except OpenAIError as exc:
            raise KnowledgeError("Embedding provider failed") from exc
        validate_vectors(vectors, len(texts), self.dimension)
        return vectors


def configured_embedder() -> Embedder:
    backend = os.environ.get("EMBEDDING_BACKEND", "fake")
    try:
        dimension = int(
            os.environ.get("EMBEDDING_DIMENSION", "64" if backend == "fake" else "1536")
        )
    except ValueError as exc:
        raise KnowledgeError("Embedding dimension must be an integer") from exc
    model = os.environ.get("EMBEDDING_MODEL", "fake-token-v1" if backend == "fake" else "")
    if backend == "fake" and model == FakeEmbedder.model:
        return FakeEmbedder(dimension)
    if backend == "openai":
        return OpenAIEmbedder(model, dimension, api_key=os.environ.get("OPENAI_API_KEY", ""))
    raise KnowledgeError("Invalid embedding backend/model configuration")
