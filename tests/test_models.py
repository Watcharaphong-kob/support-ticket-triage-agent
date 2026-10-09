import json

import httpx
from test_agent import ROOT, EmptyKnowledge, decision, ticket

from triage_agent.agent import Agent
from triage_agent.config import Settings
from triage_agent.tools import ToolDispatcher


def test_live_adapter_passes_tools_and_correlates_provider_call_ids():
    observed = []

    def handle(request):
        observed.append(json.loads(request.content))
        functions = (
            [
                {
                    "id": "provider-history",
                    "name": "get_customer_history",
                    "args": {"customer_id": "customer-001"},
                },
                {
                    "id": "provider-knowledge",
                    "name": "search_knowledge_base",
                    "args": {"query": "payment"},
                },
            ]
            if len(observed) == 1
            else decision().tool_calls
        )
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
                                    "id": c["id"],
                                    "type": "function",
                                    "function": {
                                        "name": c["name"],
                                        "arguments": json.dumps(c["args"]),
                                    },
                                }
                                for c in functions
                            ],
                        },
                    }
                ],
            },
        )

    model = Settings("test-key", "configured-gpt").chat_model(
        http_client=httpx.Client(transport=httpx.MockTransport(handle))
    )
    result = Agent(model, ToolDispatcher(ROOT / "data/customers.json", EmptyKnowledge())).triage(
        ticket()
    )
    assert result.status == "completed"
    assert [c.call_id for c in result.tool_calls] == ["provider-history", "provider-knowledge"]
    assert {t["function"]["name"] for t in observed[0]["tools"]} == {
        "get_customer_history",
        "search_knowledge_base",
        "TriageResult",
    }
    assert observed[0]["store"] is False
    assert observed[0]["model"] == "configured-gpt"
