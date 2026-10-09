"""Token-bounded Unicode-safe chunks with stable identities and source provenance."""

import hashlib
from dataclasses import dataclass

import tiktoken

from triage_agent.knowledge.database import KnowledgeError
from triage_agent.knowledge.embeddings import Embedder, validate_vectors
from triage_agent.schemas import KnowledgeArticle


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def chunk_text(text: str, size: int = 500, overlap: int = 60) -> list[str]:
    if size < 8 or not 0 <= overlap < size:
        raise KnowledgeError("Invalid chunk size/overlap")
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text, disallowed_special=())
    chunks, start = [], 0
    while start < len(tokens):
        end = min(start + size, len(tokens))
        while True:
            try:
                chunk = encoding.decode_bytes(tokens[start:end]).decode("utf-8")
                break
            except UnicodeDecodeError:
                end -= 1
                if end <= start:
                    raise KnowledgeError("Unable to split Unicode safely")
        chunks.append(chunk)
        if end == len(tokens):
            break
        next_start = max(start + 1, end - overlap)
        while next_start < end:
            try:
                encoding.decode_bytes(tokens[start:next_start]).decode("utf-8")
                break
            except UnicodeDecodeError:
                next_start += 1
        start = next_start
    return chunks


@dataclass
class PreparedArticle:
    article: KnowledgeArticle
    chunks: list[str]
    vectors: list[list[float]]


def prepare_articles(articles: list[KnowledgeArticle], embedder: Embedder) -> list[PreparedArticle]:
    if len({article.id for article in articles}) != len(articles):
        raise KnowledgeError("Duplicate source IDs in ingestion input")
    prepared = []
    for article in articles:
        chunks = chunk_text(article.content)
        vectors = embedder.embed(chunks)
        validate_vectors(vectors, len(chunks), embedder.dimension)
        prepared.append(PreparedArticle(article, chunks, vectors))
    return prepared
