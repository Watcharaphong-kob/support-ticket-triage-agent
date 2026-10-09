import httpx
import pytest
from openai import OpenAI

from triage_agent.knowledge.database import KnowledgeError
from triage_agent.knowledge.embeddings import FakeEmbedder, OpenAIEmbedder, configured_embedder
from triage_agent.knowledge.ingest import chunk_text


def test_fake_vectors_are_repeatable_and_explicitly_test_only():
    fake = FakeEmbedder()
    assert fake.model.startswith("fake-")
    assert fake.embed(["ระบบ error 500"])[0] == fake.embed(["ระบบ error 500"])[0]
    with pytest.raises(KnowledgeError):
        fake.embed([""])


def test_unicode_chunking_preserves_content_without_replacement_characters():
    text = ("ระบบเข้าไม่ได้ครับ ขึ้น error 500 😊\n\n" * 100) + "end"
    chunks = chunk_text(text, size=32, overlap=0)
    assert "".join(chunks) == text
    assert all("\ufffd" not in chunk for chunk in chunks)
    assert len(chunk_text(text)) > 1


def test_live_configuration_never_silently_falls_back(monkeypatch):
    monkeypatch.setenv("EMBEDDING_BACKEND", "openai")
    monkeypatch.setenv("EMBEDDING_MODEL", "")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(KnowledgeError):
        configured_embedder()


def test_live_adapter_sends_dimension_and_restores_response_order_without_network():
    def respond(request):
        import json

        payload = json.loads(request.content)
        assert payload["dimensions"] == 2 and payload["input"] == ["first", "second"]
        return httpx.Response(
            200,
            json={
                "object": "list",
                "model": "test-embedding",
                "usage": {"prompt_tokens": 2, "total_tokens": 2},
                "data": [
                    {"object": "embedding", "index": 1, "embedding": [0.0, 1.0]},
                    {"object": "embedding", "index": 0, "embedding": [1.0, 0.0]},
                ],
            },
        )

    embedder = OpenAIEmbedder("test-embedding", 2, api_key="test-key-not-a-real-key")
    embedder.client = OpenAI(
        api_key="test-key-not-a-real-key",
        http_client=httpx.Client(transport=httpx.MockTransport(respond)),
    )
    assert embedder.embed(["first", "second"]) == [[1.0, 0.0], [0.0, 1.0]]


def test_live_adapter_rejects_oversized_text_before_provider_request():
    def should_not_send(request):
        pytest.fail("Oversized text was sent to the provider")

    embedder = OpenAIEmbedder("test-embedding", 2, api_key="test-key-not-a-real-key")
    embedder.client = OpenAI(
        api_key="test-key-not-a-real-key",
        http_client=httpx.Client(transport=httpx.MockTransport(should_not_send)),
    )
    with pytest.raises(KnowledgeError, match="token"):
        embedder.embed(["word " * 9000])


def test_chunks_keep_sections_separate_and_repeat_heading_on_long_passages():
    text = "# Billing\npayment charges require review\n\n# Themes\ndark mode needs investigation"
    chunks = chunk_text(text)
    assert len(chunks) == 2
    assert all(not ("Billing" in c and "Themes" in c) for c in chunks)
    long = "# Billing\n" + "payment charges require review " * 400
    assert all(c.startswith("# Billing\n") for c in chunk_text(long))
