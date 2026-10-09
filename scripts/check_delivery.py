"""Check reader/source fidelity and delivered prompt/write-up without paid calls."""

import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Reader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.files, self.source = [], [], [], {}
        self.paragraph = None

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.append(values["id"])
        if "href" in values:
            href = values["href"]
            if href.startswith("#"):
                self.links.append(href[1:])
            elif ":" not in href:
                self.files.append(href.split("#", 1)[0])
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
    reader = Reader()
    reader.feed((ROOT / "ASSIGNMENT_READER.html").read_text(encoding="utf-8"))
    assert len(reader.ids) == len(set(reader.ids)), "Duplicate HTML IDs"
    assert set(reader.links) <= set(reader.ids), "Broken internal navigation"
    assert all((ROOT / file).is_file() for file in reader.files), "Broken reader file link"
    assert len(reader.source) == len(source["paragraphs"]) == 35, "Missing original paragraphs"
    for paragraph in source["paragraphs"]:
        shown = "".join(reader.source[paragraph["index"]])
        assert re.sub(r"\s+", "", shown) == re.sub(r"\s+", "", paragraph["text"]), "Changed source"
    assert len((ROOT / "docs/WRITEUP.md").read_text(encoding="utf-8").split()) <= 450
    assert (ROOT / "WRITEUP.pdf").read_bytes().startswith(b"%PDF-"), "Missing PDF"
    assert (ROOT / "prompts/system.txt").read_bytes() == (
        ROOT / "src/triage_agent/prompts/system.txt"
    ).read_bytes(), "Prompt copies differ"
    print("Delivery checks passed: 35 faithful paragraphs, reader links, prompt and write-up.")


if __name__ == "__main__":
    main()
