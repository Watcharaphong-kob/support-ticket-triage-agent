"""Deterministic checks for the offline reader, source transcription and demo artifact."""

import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Reader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.files = []
        self.source = {}
        self.paragraph = None

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.append(values["id"])
        if "href" in values and values["href"].startswith("#"):
            self.links.append(values["href"][1:])
        elif "href" in values and ":" not in values["href"]:
            self.files.append(values["href"].split("#", 1)[0])
        if "data-source-paragraph" in values:
            self.paragraph = int(values["data-source-paragraph"])
            self.source[self.paragraph] = []

    def handle_endtag(self, tag):
        if tag == "div":
            self.paragraph = None

    def handle_data(self, data):
        if self.paragraph is not None:
            self.source[self.paragraph].append(data)


def main():
    source = json.loads((ROOT / "docs/assignment_source.json").read_text(encoding="utf-8"))
    page = (ROOT / "ASSIGNMENT_READER.html").read_text(encoding="utf-8")
    reader = Reader()
    reader.feed(page)
    assert len(reader.ids) == len(set(reader.ids)), "Duplicate HTML IDs"
    aliases = {"t01", "t03", "t04", "t05"}
    assert set(reader.links) <= set(reader.ids) | aliases, "Broken internal navigation"
    assert all((ROOT / file).is_file() for file in reader.files), "Broken reader file link"
    assert len(reader.source) == len(source["paragraphs"]) == 35, "Missing original paragraphs"
    for paragraph in source["paragraphs"]:
        shown = "".join(reader.source[paragraph["index"]])
        assert re.sub(r"\s+", "", shown) == re.sub(r"\s+", "", paragraph["text"]), (
            "Changed source text"
        )
    tasks = json.loads((ROOT / "docs/project_tasks.json").read_text(encoding="utf-8"))["tasks"]
    tickets = (ROOT / "docs/TICKETS.md").read_text(encoding="utf-8")
    for task in tasks:
        assert f"## {task['id']} — {task['title']}" in tickets, "Missing consolidated ticket"
    demo = json.loads((ROOT / "examples/sample_results.json").read_text(encoding="utf-8-sig"))
    assert demo["mode"] == "offline_demo" and len(demo["results"]) == 3
    assert all(r["status"] == "completed" for r in demo["results"])
    assert len((ROOT / "docs/WRITEUP.md").read_text(encoding="utf-8").split()) <= 450
    assert (ROOT / "prompts/system.txt").read_bytes() == (
        ROOT / "src/triage_agent/prompts/system.txt"
    ).read_bytes()
    print(
        "Delivery checks passed: 35 source paragraphs, reader navigation, "
        f"{len(tasks)} tickets, 3 labeled samples."
    )


if __name__ == "__main__":
    main()
