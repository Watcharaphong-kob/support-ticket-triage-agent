"""Rebuild planning documents and the offline reader from shared task/source data."""

# Embedded HTML/CSS/JS literals intentionally retain long lines.
# ruff: noqa: E501

import html
import json
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINKS = {
    "PROJECT_TASK_PLANNER.md": "#planner",
    "TODO.md": "#todo",
    "PROJECT_SPEC.md": "#spec",
    "TECH_STACK.md": "#stack",
    "AGENT_KNOWLEDGE_SPEC.md": "#knowledge",
    "GITHUB_REPO_PLAN.md": "#github",
    "TICKETS.md": "#tickets",
}


def inline(value):
    value = html.escape(value)
    value = re.sub(r"`([^`]+)`", r"<code>\1</code>", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)

    def link(match):
        label, target = match.groups()
        target = LINKS.get(html.unescape(target), target)
        if target.startswith("docs/tickets/"):
            target = "#tickets"
        return f'<a href="{target}">{label}</a>'

    return re.sub(r"\[([^\]]+)\]\(([^\s)]+)\)", link, value)


def markdown(value):
    lines, result, index = value.splitlines(), [], 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line.startswith("```"):
            index += 1
            block = []
            while index < len(lines) and not lines[index].startswith("```"):
                block.append(lines[index])
                index += 1
            result.append("<pre><code>" + html.escape("\n".join(block)) + "</code></pre>")
            index += 1
            continue
        if line.startswith("|"):
            rows = []
            while index < len(lines) and lines[index].startswith("|"):
                cells = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", cell) for cell in cells):
                    rows.append(cells)
                index += 1
            header = "".join(f'<th scope="col">{inline(cell)}</th>' for cell in rows[0])
            body = "".join(
                "<tr>" + "".join(f"<td>{inline(cell)}</td>" for cell in row) + "</tr>"
                for row in rows[1:]
            )
            result.append(
                '<div class="table-scroll"><table><thead><tr>'
                + header
                + "</tr></thead><tbody>"
                + body
                + "</tbody></table></div>"
            )
            continue
        heading = re.match(r"^(#{1,6}) (.*)", line)
        if heading:
            level = min(len(heading[1]) + 1, 6)
            result.append(f"<h{level}>{inline(heading[2])}</h{level}>")
            index += 1
            continue
        ordered = bool(re.match(r"^\d+\. ", line))
        if line.startswith("- ") or ordered:
            tag = "ol" if ordered else "ul"
            result.append(f"<{tag}>")
            while index < len(lines):
                current = lines[index]
                if not (
                    bool(re.match(r"^\d+\. ", current)) if ordered else current.startswith("- ")
                ):
                    break
                current = re.sub(r"^\d+\. ", "", current) if ordered else current[2:]
                if current.startswith(("[x] ", "[ ] ")):
                    checked = " checked" if current.startswith("[x]") else ""
                    content = f'<input type="checkbox" disabled{checked} aria-label="Task status"> '
                    content += inline(current[4:])
                else:
                    content = inline(current)
                result.append(f"<li>{content}</li>")
                index += 1
            result.append(f"</{tag}>")
            continue
        block = [line]
        index += 1
        while index < len(lines) and lines[index].strip():
            if re.match(r"^(#|\||- |```|\d+\. )", lines[index]):
                break
            block.append(lines[index])
            index += 1
        result.append("<p>" + inline(" ".join(block)) + "</p>")
    return "\n".join(result)


def write(name, text):
    (ROOT / name).write_text(text.rstrip() + "\n", encoding="utf-8")


def blocks_to_markdown(blocks):
    text = "\n\n".join(blocks)
    return re.sub(r"(?m)(^\|.*)\n\n(?=\|)", r"\1\n", text)


def main():
    data = json.loads((ROOT / "docs/project_tasks.json").read_text(encoding="utf-8"))
    tasks = data["tasks"]
    baseline = [task for task in tasks if task["id"].startswith("T")]
    phase1 = [task for task in tasks if task["scope"] == "phase1"]
    phase2 = [task for task in tasks if task["scope"] == "phase2"]
    done = {task["id"] for task in tasks if task["status"] == "done"}
    ready = [
        task["id"]
        for task in phase1
        if task["status"] == "todo" and set(task["depends_on"]) <= done
    ]
    next_task = ready[0] if ready else "Phase 1 complete"
    assert len({task["id"] for task in tasks}) == len(tasks)
    assert sum(task["minutes"] for task in baseline) == data["baseline_minutes"]
    assert all(
        dep in {task["id"] for task in tasks} for task in tasks for dep in task["depends_on"]
    )
    date = data["date"]
    planner = [
        "# Project Task Planner",
        f"{date} · Rebuilt from docs/project_tasks.json",
        "## Current position",
        f"{len(done)} of {len(phase1)} Phase 1 tasks complete. T01 design is approved; "
        "T02 setup is verified and pushed; E01 architecture selection is approved. "
        f"Next ready task: {next_task}. GPT/tool/CLI implementation is available; see verification for live-check limits.",
        "This is the current task plan. Existing task IDs and completion evidence are preserved. "
        "Phase 1 is a Docker classic-RAG prototype using PostgreSQL + pgvector. "
        "GraphRAG is deferred to Phase 2. Selected components are not yet installed capabilities.",
        "## Spec and stack",
        "[Project spec](PROJECT_SPEC.md) defines scope, contracts and acceptance. "
        "[Tech stack](TECH_STACK.md) separates installed tools from selected Phase 1 components. "
        "[Working TODO list](TODO.md) mirrors the tasks below. "
        "[Execution tickets](TICKETS.md) record skills, plugins, steps and evidence. "
        "[RAG and GraphRAG spec](AGENT_KNOWLEDGE_SPEC.md) supplies extension details.",
        "## Phases and timing",
        "The original homework estimate was 210 minutes and the assignment recommends 150–240 minutes. "
        "Docker and real classic RAG expand that scope. A revised Phase 1 estimate is not assigned; "
        "original task minutes below are historical references, not a total for this prototype.",
        "## Phase 1 — Docker classic RAG prototype",
        "| Task | Status | Min | Dependencies | Deliverable |",
        "| --- | --- | --- | --- | --- |",
    ]
    for task in phase1:
        planner.append(
            f"| {task['id']} | {task['status']} | {task['minutes'] or 'TBD'} | "
            f"{', '.join(task['depends_on']) or '—'} | {task['title']} |"
        )
    planner += [
        "## Phase 2 — deferred GraphRAG",
        "| Task | Status | Dependencies | Deliverable |",
        "| --- | --- | --- | --- |",
    ]
    for task in phase2:
        planner.append(
            f"| {task['id']} | {task['status']} | {', '.join(task['depends_on'])} | {task['title']} |"
        )
    planner += ["## Task contracts"]
    for task in tasks:
        planner += [
            f"### {task['id']} — {task['title']}",
            f"Phase: {task['phase']}. Status: {task['status']}. "
            f"Depends on: {', '.join(task['depends_on']) or 'none'}. "
            f"Estimate: {str(task['minutes']) + ' min (historical)' if task['minutes'] else 'TBD'}.",
            "Outputs: " + ", ".join(f"`{item}`" for item in task["outputs"]) + ".",
            "Acceptance: " + task["acceptance"],
        ]
        if task.get("skills_used"):
            planner += [
                "Skills used: " + ", ".join(task["skills_used"]) + ".",
                "Plugins used: " + ", ".join(task["plugins_used"]) + ".",
                "Verification: " + task["verification"],
                f"[Execution ticket]({task['ticket']})",
            ]
    planner += [
        "## Execution rules",
        "Implement one task at a time in dependency order. Use focused failing tests before "
        "behavior changes and record actual verification. Keep prompts/tools/model adapters "
        "separate. Do not mark installed libraries as working agent features. "
        "Review architecture changes before extension implementation.",
        "Consult ask-matt before and after each task to select the testing/review route. "
        "Record fresh evidence before marking completion; see docs/TASK_WORKFLOW.md. "
        "The completed T03 plan is docs/superpowers/plans/2026-10-09-t03-bilingual-fixtures.md; "
        f"next ready task: {next_task}.",
        "T02 evidence: docs/T02_SETUP_STATUS.md. Repository/worktree/submission workflow: "
        "[GitHub plan](GITHUB_REPO_PLAN.md). Preserve customer uncertainty and source citations.",
    ]
    write("PROJECT_TASK_PLANNER.md", blocks_to_markdown(planner))
    todo = [
        "# Project TODO",
        f"{date} · {len(done)}/{len(phase1)} Phase 1 tasks done · Next: {next_task}",
        "[Spec](PROJECT_SPEC.md) · [Stack](TECH_STACK.md) · [Detailed planner](PROJECT_TASK_PLANNER.md)",
        "[Tickets with skills, plugins and steps](TICKETS.md)",
        "Checked tasks record completed setup/design and the user's E01 architecture decision. "
        "Classic RAG and Docker are selected for Phase 1; GraphRAG is deferred to Phase 2. "
        "Task data lives in docs/project_tasks.json; rebuild with uv run python scripts/build_planner.py.",
    ]
    phases = list(dict.fromkeys(task["phase"] for task in tasks))
    for phase in phases:
        todo.append("## " + phase)
        for task in [task for task in tasks if task["phase"] == phase]:
            tick = "x" if task["status"] == "done" else " "
            todo.append(
                f"- [{tick}] **{task['id']} — {task['title']}** ({task['status']}): {task['acceptance']}"
            )
        todo.append("")
    todo += [
        "## Before submission",
        "Follow T12 acceptance and the final verification record. "
        "Verification covers fixtures, schemas, Docker, ingestion, retrieval, GPT adapter contracts, agent and CLI. "
        "Live provider calls have not run. "
        "The historical 210-minute estimate does not cover the expanded Phase 1 scope.",
    ]
    write("TODO.md", "\n\n".join(todo))
    ticket_blocks = [
        "# Execution Tickets",
        f"{date} · Local project tickets",
        "Each ticket records dependencies, acceptance, skills/plugins and simple steps. "
        "Completed steps are evidence; planned steps are not claimed as executed.",
    ]
    (ROOT / "docs/tickets").mkdir(exist_ok=True)
    if data.get("github_issue"):
        ticket_blocks.append(
            f"[GitHub Phase 1 tracking issue]({data['github_issue']}) · ready-for-agent. "
            "The local task tickets below contain per-task execution details."
        )
    for task in tasks:
        body = [
            f"# {task['id']} — {task['title']}",
            f"Status: {task['status']}. Scope: {task['scope']}. "
            f"Dependencies: {', '.join(task['depends_on']) or 'none'}.",
            "## Acceptance",
            task["acceptance"],
            "## Skills and plugins",
        ]
        if task.get("steps_done"):
            body += [
                "Skills used: " + ", ".join(task["skills_used"]) + ".",
                "Plugins used: " + ", ".join(task["plugins_used"]) + ".",
                "Tools: PowerShell, uv, pytest, Ruff, Docker Compose. "
                + (
                    "GitHub connector published the tracking issue."
                    if task["id"] == "T05"
                    else "No external app connector used for this task."
                ),
                "## Steps performed",
            ]
            body += [f"{i}. {step}" for i, step in enumerate(task["steps_done"], 1)]
            body += [
                "## Verification",
                task["verification"],
                "Implementation commit: " + task["implementation_commit"] + ".",
            ]
        elif task["status"] == "done":
            body += [
                "Historical task; skill usage was not recorded in this ticket format.",
                "## Evidence",
                "See the task outputs and existing setup/design evidence.",
            ]
        else:
            body += [
                "Planned skills: ask-matt before/after, implement, tdd, code-review, "
                "Superpowers execution and verification. Not executed yet.",
                "## Planned steps",
                "1. Read dependencies and acceptance; consult ask-matt.",
                "2. Add a failing behavior check at the agreed public boundary.",
                "3. Implement the smallest required change.",
                "4. Consult ask-matt, test and review; record evidence before completion.",
            ]
        text = "\n\n".join(body)
        write(f"docs/tickets/{task['id']}.md", text)
        ticket_blocks += [text.replace("# ", "## ", 1)]
    write("TICKETS.md", "\n\n".join(ticket_blocks))
    lock = tomllib.loads((ROOT / "uv.lock").read_text(encoding="utf-8"))
    versions = {package["name"]: package["version"] for package in lock["package"]}
    stack = [
        "# Tech Stack",
        f"{date} · Versions read from committed uv.lock",
        "## Installed baseline",
        "| Component | Technology | Version / choice | Status |",
        "| --- | --- | --- | --- |",
        "| Language | Python | >=3.11; development default 3.12 | Package ready |",
        "| Packages | uv | pyproject.toml + uv.lock + ignored .venv | Ready |",
        f"| Model client | openai | {versions['openai']} | GPT adapter implemented; mocked HTTP verified |",
        f"| Validation | pydantic | {versions['pydantic']} | Installed; schemas T04 |",
        "| CLI | argparse | Python standard library | JSON batch processing implemented |",
        f"| Tests | pytest | {versions['pytest']} | 8 setup tests passed at T02 |",
        f"| Lint / format | ruff | {versions['ruff']} | T02 checks passed |",
        "| Build | setuptools | >=77 build backend | Wheel/source build verified |",
        "| Source control | Git + private GitHub | main + feat/triage-agent | Repository ready |",
        "## Selected Phase 1 components",
        "| Area | Technology / decision | Status |",
        "| --- | --- | --- |",
        "| Main agent | openai SDK with explicit bounded tool loop | Implemented; 6 requests / 8 tool executions |",
        "| Customer / ticket data | Synthetic UTF-8 JSON fixtures | T03 implemented |",
        "| Runtime | Docker Engine 28.5.1 + Compose 2.40.0; Python 3.12.14 image + uv 0.12.6 | Startup verified |",
        "| Knowledge database | PostgreSQL 17 + pgvector 0.8.7 | Healthy Docker service; migrations verified |",
        f"| Database client | psycopg {versions.get('psycopg', 'pending')} + pgvector {versions.get('pgvector', 'pending')} | uv-locked |",
        "| Retrieval | Classic RAG; exact cosine search, top 5, metadata filters, 0.2 ranking cutoff | Real DB tests passed |",
        f"| Chunk tokenizer | tiktoken {versions.get('tiktoken', 'pending')}; cl100k_base | Unicode-safe 500 tokens / 60 overlap |",
        "| Embeddings | Fake lexical vectors by default; opt-in OpenAI model/dimension | Adapter tested with mock HTTP; live semantic quality pending |",
        "| Phase 2 | GraphRAG; backend decision in next phase | Deferred; no graph dependencies now |",
        "| CI | GitHub Actions + uv offline checks | Configured; local-equivalent checks verified |",
        "## Stack decisions",
        "Phase 1 is a prototype using one knowledge database and the existing model SDK. "
        "Classic RAG retrieves passages; GraphRAG relationships and traversal belong to Phase 2. "
        "Pin compatible Docker images and new dependencies during setup. "
        "Details are in [knowledge-system spec](AGENT_KNOWLEDGE_SPEC.md).",
        "## Configuration and commands",
        "GPT model: OPENAI_MODEL. Key: OPENAI_API_KEY. "
        "No hard-coded model or actual key in the submission. Help/version/offline tests need no key.",
        "```powershell\nuv sync --locked\nuv run --locked triage-agent --help\n"
        "uv run --locked pytest\nuv run --locked ruff check .\n"
        "uv run --locked ruff format --check .\nuv build\n"
        "uv run --locked python scripts/build_planner.py\n```",
    ]
    write("TECH_STACK.md", blocks_to_markdown(stack))
    source = json.loads((ROOT / "docs/assignment_source.json").read_text(encoding="utf-8"))
    original = [
        "<h2>Original assignment</h2><p class=note>Complete source transcription; "
        "message spacing is reformatted. Assignment requirements are reference material; "
        "the current spec records the user's selected implementation scope.</p>"
    ]
    for paragraph in source["paragraphs"]:
        number, text = paragraph["index"], paragraph["text"]
        if number in (33, 36, 39):
            body = "".join(
                '<p class="message">' + html.escape(part) + "</p>"
                for part in re.split(r"(?=Message [1-4] \()", text)
                if part
            )
        elif number in (0, 13, 14, 21, 30, 32, 35, 38):
            body = "<h3>" + html.escape(text) + "</h3>"
        else:
            body = "<p>" + html.escape(text) + "</p>"
        original.append(f'<div data-source-paragraph="{number}">{body}</div>')
    overview = f"""<div class="eyebrow">PROJECT WORKSPACE · {date}</div>
<h2>Support Ticket<br>Triage Agent</h2><p class="lead">The assignment, spec, stack and execution plan in one offline reader.</p>
<div class="stats"><div><b>{len(done)}/{len(phase1)}</b><span>Phase 1 tasks complete</span></div><div><b>Classic RAG</b><span>Docker + PostgreSQL + pgvector</span></div><div><b>Prototype</b><span>GraphRAG deferred to Phase 2</span></div></div>
<div class="note">GPT prompt, bounded agent loop, JSON CLI, Docker classic RAG and both tools implemented; see Tickets for evidence. Next: {next_task}. Live embeddings not verified.</div>
<div class="tiles"><a href="#spec"><b>Project spec</b><span>Scope, contracts and acceptance</span></a><a href="#stack"><b>Tech stack</b><span>Installed tools and proposed choices</span></a><a href="#todo"><b>TODO list</b><span>One shared list; verified status</span></a><a href="#original"><b>Original assignment</b><span>All conversations, including Thai</span></a></div>
{markdown((ROOT / "ASSIGNMENT_SUMMARY.md").read_text(encoding="utf-8"))}"""
    pages = [
        ("overview", "Overview", overview),
        (
            "planner",
            "Task planner",
            markdown((ROOT / "PROJECT_TASK_PLANNER.md").read_text(encoding="utf-8"))
            + "<details><summary>T03 implementation plan and checklist</summary>"
            + markdown(
                (ROOT / "docs/superpowers/plans/2026-10-09-t03-bilingual-fixtures.md").read_text(
                    encoding="utf-8"
                )
            )
            + "</details><details><summary>Before/after task checking workflow</summary>"
            + markdown((ROOT / "docs/TASK_WORKFLOW.md").read_text(encoding="utf-8"))
            + "</details>",
        ),
        ("todo", "TODO list", markdown((ROOT / "TODO.md").read_text(encoding="utf-8"))),
        ("tickets", "Tickets", markdown((ROOT / "TICKETS.md").read_text(encoding="utf-8"))),
        (
            "spec",
            "Spec",
            markdown((ROOT / "PROJECT_SPEC.md").read_text(encoding="utf-8"))
            + "<details><summary>Main Word assignment — requirement traceability</summary>"
            + markdown((ROOT / "docs/ASSIGNMENT_REQUIREMENTS.md").read_text(encoding="utf-8"))
            + "</details><details><summary>Support-ticket glossary</summary>"
            + markdown((ROOT / "GLOSSARY.md").read_text(encoding="utf-8"))
            + "</details>"
            + "<details><summary>Historical T01 contracts and design</summary><p>The current Phase 1 spec supersedes the original mock-only knowledge scope. Triage policies and output contracts remain applicable.</p>"
            + markdown(
                (ROOT / "docs/superpowers/specs/2026-10-09-ticket-triage-design.md").read_text(
                    encoding="utf-8"
                )
            )
            + "</details>",
        ),
        ("stack", "Tech stack", markdown((ROOT / "TECH_STACK.md").read_text(encoding="utf-8"))),
        (
            "knowledge",
            "Knowledge system",
            markdown((ROOT / "AGENT_KNOWLEDGE_SPEC.md").read_text(encoding="utf-8")),
        ),
        (
            "github",
            "GitHub plan",
            markdown((ROOT / "GITHUB_REPO_PLAN.md").read_text(encoding="utf-8")),
        ),
        (
            "t02",
            "Verified setup",
            markdown((ROOT / "docs/T02_SETUP_STATUS.md").read_text(encoding="utf-8")),
        ),
        ("original", "Original assignment", "\n".join(original)),
    ]
    nav = "".join(f'<a href="#{key}">{label}</a>' for key, label, _ in pages)
    content = "".join(
        f'<section class="page" id="{key}" tabindex="-1">{body}</section>' for key, _, body in pages
    )
    css = """
:root{--ink:#183039;--muted:#5d737a;--accent:#116b65;--line:#dbe5e7;--bg:#eef3f3}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.75 'Segoe UI','Leelawadee UI',Tahoma,sans-serif}a{color:var(--accent)}
.layout{max-width:1400px;margin:auto;display:grid;grid-template-columns:235px minmax(0,1fr);gap:28px;padding:28px}aside{position:sticky;top:28px;align-self:start}.brand{font-size:20px;font-weight:750;margin-bottom:2px}.sub{color:var(--muted);font-size:12px;letter-spacing:.08em;margin-bottom:24px}nav a{display:block;padding:9px 14px;margin:4px 0;border-radius:9px;color:var(--ink);text-decoration:none;font-size:14px}nav a:hover,nav a[aria-current=page]{background:#d4e9e3;color:#08524d;font-weight:650}.aside-note{font-size:12px;color:var(--muted);margin:26px 14px}main{min-width:0}.page{padding:36px 42px;background:white;border:1px solid var(--line);border-radius:16px;margin-bottom:24px;box-shadow:0 3px 20px #193b4310}.enhanced .page{display:none}.enhanced .page.active{display:block}.eyebrow{color:var(--accent);letter-spacing:.13em;font-size:12px;font-weight:700}h2{font-size:32px;line-height:1.3;margin:8px 0 22px}#overview>h2{font-size:clamp(36px,5vw,58px);letter-spacing:-.025em;line-height:1.08}h3{font-size:22px;line-height:1.4;margin:30px 0 14px}h4{font-size:18px;line-height:1.45;margin:26px 0 12px}p{margin:12px 0}.lead{font-size:18px;color:var(--muted)}.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:26px 0}.stats>div{border:1px solid var(--line);border-radius:11px;padding:18px;background:#f6f9f8}.stats b{display:block;font-size:25px}.stats span{font-size:12px;color:var(--muted)}.note{padding:16px 20px;border-left:4px solid var(--accent);background:#edf6f2;border-radius:0 8px 8px 0;margin:20px 0}.tiles{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin:26px 0}.tiles a{display:block;padding:20px;border:1px solid var(--line);border-radius:10px;text-decoration:none}.tiles a:hover{background:#edf6f2}.tiles b,.tiles span{display:block}.tiles span{font-size:13px;color:var(--muted)}ul,ol{padding-left:24px}li{margin:10px 0}input[type=checkbox]{accent-color:var(--accent);margin-right:7px}table{width:100%;border-collapse:collapse;font-size:14px;line-height:1.6}th,td{padding:12px 14px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line);min-width:95px}th{background:#e8f0ef}tbody tr:nth-child(even){background:#f9fbfb}.table-scroll{overflow:auto;margin:20px 0}pre{background:#173039;color:#e4f2f2;padding:20px;border-radius:10px;overflow:auto;font-size:13px;line-height:1.65}code{font-family:Consolas,monospace;overflow-wrap:anywhere}.message{background:#f3f7f9;padding:18px;border-left:3px solid #8caeb7;white-space:pre-wrap;overflow-wrap:anywhere}details{margin:24px 0;border:1px solid var(--line);padding:18px;border-radius:10px}summary{cursor:pointer;font-weight:650}.skip{position:absolute;left:-9999px}.skip:focus{left:12px;top:12px;background:white;padding:10px;z-index:2}footer{font-size:12px;color:var(--muted);padding:6px}
@media(max-width:900px){.layout{grid-template-columns:1fr;padding:14px;gap:14px}aside{position:static}.sub,.aside-note{display:none}nav{display:flex;flex-wrap:wrap;gap:3px}nav a{background:#e5eded;font-size:13px;padding:6px 10px}.page{padding:24px 20px}.stats{gap:7px}.stats>div{padding:12px}.stats b{font-size:21px}}
@media(max-width:480px){.tiles{grid-template-columns:1fr}.stats{grid-template-columns:1fr}.stats>div{display:flex;gap:16px;align-items:center}}
@media print{body{background:white;font-size:10pt}.layout{display:block;padding:0}aside,footer,.skip{display:none}.page,.enhanced .page{display:block!important;box-shadow:none;border:0;padding:0;break-before:page}.page:first-child{break-before:auto}h2,h3,h4{break-after:avoid}tr,.message{break-inside:avoid}.table-scroll{overflow:visible}table{font-size:9pt}pre{white-space:pre-wrap;background:#f1f4f5;color:var(--ink)}.tiles{display:none}}
"""
    script = """
const aliases={summary:'overview',t01:'spec','tech-stack':'stack','implementation-spec':'spec'};
function showPage(){let key=location.hash.slice(1)||'overview';key=aliases[key]||key;
if(!document.getElementById(key)?.classList.contains('page'))key='overview';
document.querySelectorAll('.page').forEach(p=>p.classList.toggle('active',p.id===key));
document.querySelectorAll('nav a').forEach(a=>{if(a.hash==='#'+key)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')});
document.title='OOCA · '+(document.querySelector('nav a[aria-current]')?.textContent||'Overview');}
document.body.classList.add('enhanced');showPage();window.addEventListener('hashchange',()=>{showPage();window.scrollTo(0,0)});
window.addEventListener('beforeprint',()=>document.querySelectorAll('details').forEach(d=>{d.dataset.wasOpen=String(d.open);d.open=true}));
window.addEventListener('afterprint',()=>document.querySelectorAll('details').forEach(d=>{d.open=d.dataset.wasOpen==='true';delete d.dataset.wasOpen}));
"""
    write(
        "ASSIGNMENT_READER.html",
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        "<title>OOCA · Project planner</title><style>" + css + "</style></head><body>"
        '<a class="skip" href="#overview">Skip to content</a><div class="layout"><aside>'
        '<div class="brand">OOCA Assignment</div><div class="sub">SUPPORT TICKET TRIAGE</div>'
        '<nav aria-label="Document views">'
        + nav
        + f'</nav><div class="aside-note">{len(done)}/{len(phase1)} Phase 1 tasks done<br>'
        "Offline reader · Ctrl+P to print<br>Task data: docs/project_tasks.json</div></aside><main>"
        + content
        + "<footer>Generated from shared task data and source documents. "
        "Document links work offline; external reference links require a connection.</footer>"
        "</main></div><script>" + script + "</script></body></html>",
    )
    print(
        f"Rebuilt planner, TODO, stack and reader: {len(phase1)} Phase 1 tasks, "
        f"{len(phase2)} deferred Phase 2 task, {len(done)} done."
    )


if __name__ == "__main__":
    main()
