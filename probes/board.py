"""Research board CLI — a lightweight arcs->items tracker for the lab.

Source of truth is board/board.json (fixed schema: a top-level "states"
dict of valid item states + their meanings, and "arcs", each holding
"items" with a state, links, and a dated notes[] log). This script only
reads/writes that file and regenerates BOARD.md, a read-only rendered
mirror for GitHub.

Usage:
    .venv/bin/python probes/board.py                 # overview (all arcs)
    .venv/bin/python probes/board.py ls               # same
    .venv/bin/python probes/board.py ls <arc-id>       # one arc, in detail
    .venv/bin/python probes/board.py add <arc-id> "title" [--state hunch] [--note "text"]
    .venv/bin/python probes/board.py mv <item-id> <state> [message words...]
    .venv/bin/python probes/board.py note <item-id> "text"
    .venv/bin/python probes/board.py arc add <id> "title" "question" [--status active]

Every mutating command rewrites board.json (2-space indent, trailing
newline, existing key order — dict insertion order from json.loads
mirrors the file, and new records are built with matching key order so
nothing reshuffles) and regenerates BOARD.md. Dates are
datetime.date.today().isoformat(). Unknown ids/states are a clear error
on stderr + exit 1, before any write.

Stdlib only.
"""

import argparse
import datetime
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).parent.parent
BOARD_JSON = ROOT / "board" / "board.json"
BOARD_MD = ROOT / "BOARD.md"
REGEN_CMD = ".venv/bin/python probes/board.py"

GLYPH = {
    "hunch": "○",
    "queued": "◇",
    "hot": "●",
    "landed": "✓",
    "dissolved": "∅",
    "parked": "‖",
    "dropped": "✗",
}


def today() -> str:
    return datetime.date.today().isoformat()


def die(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def glyph(state: str) -> str:
    return GLYPH.get(state, "?")


def load() -> dict:
    if not BOARD_JSON.exists():
        die(f"no board at {BOARD_JSON}")
    return json.loads(BOARD_JSON.read_text())


def save(board: dict) -> None:
    board["updated"] = today()
    BOARD_JSON.write_text(
        json.dumps(board, indent=2, ensure_ascii=False) + "\n")
    BOARD_MD.write_text(render_md(board))


def find_arc(board: dict, arc_id: str) -> dict | None:
    return next((a for a in board["arcs"] if a["id"] == arc_id), None)


def find_item(board: dict, item_id: str) -> tuple[dict | None, dict | None]:
    for arc in board["arcs"]:
        for item in arc["items"]:
            if item["id"] == item_id:
                return arc, item
    return None, None


def next_item_id(arc: dict) -> str:
    prefix = arc["id"] + "-"
    nums = [int(i["id"][len(prefix):]) for i in arc["items"]
            if i["id"].startswith(prefix) and i["id"][len(prefix):].isdigit()]
    return f"{arc['id']}-{(max(nums) + 1) if nums else 1:02d}"


def latest_note(item: dict) -> dict | None:
    return item["notes"][-1] if item["notes"] else None


# ---- commands ----

def cmd_ls(board: dict, arc_id: str | None) -> None:
    if arc_id is None:
        print(f"J-space research board — updated {board['updated']}\n")
        for arc in board["arcs"]:
            print(f"{arc['id']:<10} {arc['title']}  [{arc['status']}]")
            print(f"           {arc['question']}")
            for item in arc["items"]:
                note = latest_note(item)
                when = note["date"] if note else "—"
                print(f"    {glyph(item['state'])} {item['id']:<12} "
                      f"{item['title']:<62} {when}")
            print()
        return

    arc = find_arc(board, arc_id)
    if arc is None:
        die(f"no such arc {arc_id!r}")
    print(f"{arc['title']}  [{arc['status']}]  ({arc['id']})")
    print(f"{arc['question']}\n")
    for item in arc["items"]:
        print(f"{glyph(item['state'])} {item['id']}  {item['title']}  "
              f"[{item['state']}]")
        if item["links"]:
            print(f"    links: {', '.join(item['links'])}")
        for note in item["notes"]:
            print(f"    {note['date']}  {note['text']}")
        print()


def cmd_add(board: dict, arc_id: str, title: str, state: str,
            note: str | None) -> None:
    arc = find_arc(board, arc_id)
    if arc is None:
        die(f"no such arc {arc_id!r}")
    if state not in board["states"]:
        die(f"unknown state {state!r} (valid: {', '.join(board['states'])})")
    item_id = next_item_id(arc)
    notes = [{"date": today(), "text": note}] if note else []
    item = {"id": item_id, "title": title, "state": state, "links": [],
            "notes": notes}
    arc["items"].append(item)
    save(board)
    print(f"added {item_id}: {title}  [{state}]")


def cmd_mv(board: dict, item_id: str, state: str, message: list[str]) -> None:
    arc, item = find_item(board, item_id)
    if item is None:
        die(f"no such item {item_id!r}")
    if state not in board["states"]:
        die(f"unknown state {state!r} (valid: {', '.join(board['states'])})")
    text = f"→ {state}"
    if message:
        text += ": " + " ".join(message)
    item["state"] = state
    item["notes"].append({"date": today(), "text": text})
    save(board)
    print(f"{item_id}: {glyph(state)} {state}")


def cmd_note(board: dict, item_id: str, text: str) -> None:
    _, item = find_item(board, item_id)
    if item is None:
        die(f"no such item {item_id!r}")
    item["notes"].append({"date": today(), "text": text})
    save(board)
    print(f"{item_id}: noted")


def cmd_arc_add(board: dict, arc_id: str, title: str, question: str,
                 status: str) -> None:
    if find_arc(board, arc_id) is not None:
        die(f"arc {arc_id!r} already exists")
    arc = {"id": arc_id, "title": title, "status": status,
           "question": question, "items": []}
    board["arcs"].append(arc)
    save(board)
    print(f"added arc {arc_id}: {title}  [{status}]")


# ---- BOARD.md rendering ----

def _md_escape(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ")


def render_md(board: dict) -> str:
    legend = " · ".join(f"{glyph(s)} {s}" for s in board["states"])
    lines = [
        "# Research board",
        "",
        f"_Generated from `board/board.json` — do not hand-edit; regenerate "
        f"with `{REGEN_CMD}` (any `add`/`mv`/`note`/`arc add` does this "
        f"automatically)._",
        "",
        f"Updated: {board['updated']}",
        "",
        f"Legend: {legend}",
        "",
    ]
    for arc in board["arcs"]:
        lines.append(f"## {arc['title']}")
        lines.append("")
        lines.append(f"*{arc['status']} — {arc['question']}*")
        lines.append("")
        if arc["items"]:
            lines.append("| | id | title | latest note |")
            lines.append("|---|---|---|---|")
            for item in arc["items"]:
                note = latest_note(item)
                latest = (f"{note['date']} {_md_escape(note['text'])}"
                          if note else "—")
                lines.append(
                    f"| {glyph(item['state'])} | {item['id']} | "
                    f"{_md_escape(item['title'])} | {latest} |")
        else:
            lines.append("_(no items yet)_")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


# ---- CLI ----

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="board.py", description="J-space research board")
    sub = p.add_subparsers(dest="cmd")

    p_ls = sub.add_parser("ls", help="overview, or one arc in detail")
    p_ls.add_argument("arc_id", nargs="?")

    p_add = sub.add_parser("add", help="new item in an arc")
    p_add.add_argument("arc_id")
    p_add.add_argument("title")
    p_add.add_argument("--state", default="hunch")
    p_add.add_argument("--note")

    p_mv = sub.add_parser("mv", help="change an item's state")
    p_mv.add_argument("item_id")
    p_mv.add_argument("state")
    p_mv.add_argument("message", nargs="*")

    p_note = sub.add_parser("note", help="append a dated note to an item")
    p_note.add_argument("item_id")
    p_note.add_argument("text")

    p_arc = sub.add_parser("arc", help="arc-level commands")
    arc_sub = p_arc.add_subparsers(dest="arc_cmd")
    p_arc_add = arc_sub.add_parser("add", help="new arc")
    p_arc_add.add_argument("arc_id")
    p_arc_add.add_argument("title")
    p_arc_add.add_argument("question")
    p_arc_add.add_argument("--status", default="active")

    return p


def main() -> None:
    args = build_parser().parse_args()
    board = load()
    cmd = args.cmd or "ls"

    if cmd == "ls":
        cmd_ls(board, getattr(args, "arc_id", None))
    elif cmd == "add":
        cmd_add(board, args.arc_id, args.title, args.state, args.note)
    elif cmd == "mv":
        cmd_mv(board, args.item_id, args.state, args.message)
    elif cmd == "note":
        cmd_note(board, args.item_id, args.text)
    elif cmd == "arc":
        if args.arc_cmd != "add":
            die('usage: board.py arc add <id> "title" "question" '
                '[--status active]')
        cmd_arc_add(board, args.arc_id, args.title, args.question,
                    args.status)
    else:
        die(f"unknown command {cmd!r}")


if __name__ == "__main__":
    main()
