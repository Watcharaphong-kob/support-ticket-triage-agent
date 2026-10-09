import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_ticket_conversations_match_assignment():
    source = json.loads((ROOT / "docs/assignment_source.json").read_text(encoding="utf-8"))
    paragraphs = {p["index"]: p["text"] for p in source["paragraphs"]}
    tickets = json.loads((ROOT / "data/sample_tickets.json").read_text(encoding="utf-8"))
    assert len(tickets) == 3
    for sample, index in enumerate((33, 36, 39), 1):
        ticket = tickets[sample - 1]
        expected = re.findall(
            r'Message (\d) \((.*?)\):"(.*?)"(?:\(Thai: (.*?)\))?', paragraphs[index]
        )
        actual = [
            (str(m["sequence"]), m["relative_time"], m["text"], m["supplied_translation"] or "")
            for m in ticket["messages"]
        ]
        assert actual == expected
        assert len(actual) == 4
        assert ticket["source_sample"] == sample
        assert ticket["is_synthetic_id"] is True
        assert ticket["customer_info"] == paragraphs[index - 1].split("Customer info: ", 1)[1]
        assert not any("timestamp" in m for m in ticket["messages"])


def test_customers_preserve_known_context_and_synthetic_links():
    tickets = json.loads((ROOT / "data/sample_tickets.json").read_text(encoding="utf-8"))
    customers = json.loads((ROOT / "data/customers.json").read_text(encoding="utf-8"))
    assert len(customers) == len({c["customer_id"] for c in customers}) == 3
    assert [c["customer_id"] for c in customers] == [t["customer_id"] for t in tickets]
    assert [(c["plan"], c["tenure_months"]) for c in customers] == [
        ("Free", 4),
        ("Enterprise", 8),
        ("Pro", 5),
    ]
    assert [(c["region"], c["seats"]) for c in customers] == [
        (None, None),
        ("Thailand", 45),
        (None, None),
    ]
    assert all(c["is_synthetic"] for c in customers)
    assert "first critical issue" in customers[1]["prior_support_summary"]
