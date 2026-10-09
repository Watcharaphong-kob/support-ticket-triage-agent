import json

import httpx
import pytest
from openai import OpenAI

from triage_agent.models import ModelError, OpenAIModel
from triage_agent.tools import TOOL_DEFINITIONS


def test_live_adapter_passes_tools_and_correlates_provider_call_ids():
    observed = []

    def handle(request):
        observed.append(json.loads(request.content))
        return httpx.Response(
            200,
            json={
                "id": "completion",
                "object": "chat.completion",
                "created": 0,
                "model": "configured-gpt",
                "choices": [
                    {
                        "index": 0,
                        "finish_reason": "tool_calls",
                        "message": {
                            "role": "assistant",
                            "content": None,
                            "tool_calls": [
                                {
                                    "id": "provider-call",
                                    "type": "function",
                                    "function": {
                                        "name": "get_customer_history",
                                        "arguments": '{"customer_id":"customer-001"}',
                                    },
                                }
                            ],
                        },
                    }
                ],
            },
        )

    client = OpenAI(
        api_key="test-key",
        max_retries=0,
        timeout=30,
        http_client=httpx.Client(transport=httpx.MockTransport(handle)),
    )
    model = OpenAIModel("test-key", "configured-gpt", client=client)
    result = model.complete([{"role": "user", "content": "Return JSON"}], TOOL_DEFINITIONS)
    assert result.calls[0].id == "provider-call"
    assert observed[0]["tools"] == TOOL_DEFINITIONS
    assert observed[0]["response_format"] == {"type": "json_object"}
    assert observed[0]["model"] == "configured-gpt"
    assert observed[0]["store"] is False


@pytest.mark.parametrize("status,transient", [(401, False), (429, True), (500, True)])
def test_provider_errors_are_safe_and_sdk_does_not_retry(status, transient):
    requests = []

    def handle(request):
        requests.append(request)
        return httpx.Response(status, json={"error": {"message": "sensitive-provider-detail"}})

    client = OpenAI(
        api_key="test-key",
        max_retries=0,
        http_client=httpx.Client(transport=httpx.MockTransport(handle)),
    )
    with pytest.raises(ModelError) as caught:
        OpenAIModel("test-key", "configured-gpt", client=client).complete([], TOOL_DEFINITIONS)
    assert caught.value.transient is transient
    assert "sensitive" not in str(caught.value)
    assert len(requests) == 1
