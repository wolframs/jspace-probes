"""The plain-language layer: inventory, coverage, and conformance.

The site's prose was written by Claude instances for Claude instances. It
is accurate and unreadable. This module manages a parallel PLAIN layer —
ASD-STE100-shaped summaries that carry the same claims in language a
first-time reader can parse in 30 seconds — without touching the
originals, which stay exactly as written and move into a "research notes"
container on every page (see PLAIN-LANGUAGE.md for the house standard).

Surfaces and where the plain copy lives:

    results/<id>/thoughts.md   -> results/<id>/plain.md
    CONCLUSIONS.md             -> plain/conclusions.md
    dashboard/findings.json    -> same file, `pt`/`pb`/`pdesc` fields
    app.js unit overviews      -> plain/units.json
    record titles              -> plain/titles.json
    GLOSSARY.md terms of art   -> plain/terms.json (the controlled list)

Subcommands:

    inventory   what exists, what it weighs, what still lacks plain copy
    check       ASD-STE100 conformance over the plain layer
    terms       audit plain/terms.json against the corpus
    stats       one-line summary for the close-out

Usage: .venv/bin/python probes/plain.py inventory [--json]
"""

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent.parent
RESULTS = ROOT / "results"
PLAIN = ROOT / "plain"
DASH = ROOT / "dashboard"


def load_index() -> list[dict]:
    return json.loads((RESULTS / "index.json").read_text())


def words(text: str) -> int:
    return len(text.split())


def strip_md(text: str) -> str:
    """Drop code fences, inline code, links, and headings markers."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"^\s{0,3}#{1,6}\s*", "", text, flags=re.M)
    text = re.sub(r"[*_>]+", "", text)
    return text


def inventory() -> dict:
    index = load_index()
    recs = []
    for e in index:
        rid = e["id"]
        t = RESULTS / rid / "thoughts.md"
        p = RESULTS / rid / "plain.md"
        recs.append({
            "id": rid, "unit": e["unit"], "model": e["model"],
            "title": e["title"],
            "thoughts_words": words(t.read_text()) if t.exists() else 0,
            "has_thoughts": t.exists(),
            "has_plain": p.exists(),
            "plain_words": words(p.read_text()) if p.exists() else 0,
        })

    findings = json.loads((DASH / "findings.json").read_text())
    cards = [i for th in findings["themes"] for i in th["items"]]
    surfaces = {
        "records": {
            "n": len(recs),
            "with_thoughts": sum(r["has_thoughts"] for r in recs),
            "with_plain": sum(r["has_plain"] for r in recs),
            "thoughts_words": sum(r["thoughts_words"] for r in recs),
            "plain_words": sum(r["plain_words"] for r in recs),
        },
        "findings": {
            "themes": len(findings["themes"]),
            "cards": len(cards),
            "themes_plain": sum("pdesc" in th for th in findings["themes"]),
            "cards_plain": sum("pb" in i for i in cards),
            "words": sum(words(i.get("b", "")) for i in cards),
        },
        "essay": {
            "words": words((ROOT / "CONCLUSIONS.md").read_text()),
            "has_plain": (PLAIN / "conclusions.md").exists(),
            "plain_words": (words((PLAIN / "conclusions.md").read_text())
                            if (PLAIN / "conclusions.md").exists() else 0),
        },
        "units": {
            "has_plain": (PLAIN / "units.json").exists(),
            # the file is {note, units:{...}} — count the units, not the keys
            "n_plain": (len(json.loads((PLAIN / "units.json").read_text())
                            .get("units", {}))
                        if (PLAIN / "units.json").exists() else 0),
        },
        "terms": {
            "has_terms": (PLAIN / "terms.json").exists(),
            "n": (len(json.loads((PLAIN / "terms.json").read_text())["terms"])
                  if (PLAIN / "terms.json").exists() else 0),
        },
    }
    return {"surfaces": surfaces, "records": recs}


def cmd_inventory(args):
    inv = inventory()
    if args.json:
        print(json.dumps(inv, indent=1))
        return
    s = inv["surfaces"]
    r = s["records"]
    print("PLAIN-LAYER INVENTORY")
    print(f"  records          {r['with_plain']}/{r['n']} have plain.md "
          f"({r['thoughts_words']:,} words of thoughts -> "
          f"{r['plain_words']:,} words plain)")
    print(f"  findings cards   {s['findings']['cards_plain']}/"
          f"{s['findings']['cards']} plain "
          f"({s['findings']['words']:,} words original)")
    print(f"  themes           {s['findings']['themes_plain']}/"
          f"{s['findings']['themes']} plain")
    print(f"  essay            {'yes' if s['essay']['has_plain'] else 'NO'} "
          f"({s['essay']['words']:,} words original -> "
          f"{s['essay']['plain_words']:,} plain)")
    print(f"  unit summaries   {s['units']['n_plain']} written")
    print(f"  glossary terms   {s['terms']['n']} in plain/terms.json")
    missing = [x["id"] for x in inv["records"]
               if x["has_thoughts"] and not x["has_plain"]]
    print(f"\n  {len(missing)} records still need plain.md")
    if missing and args.list_missing:
        for m in missing:
            print("   -", m)


def cmd_stats(args):
    inv = inventory()
    r = inv["surfaces"]["records"]
    pct = 100 * r["with_plain"] / max(r["with_thoughts"], 1)
    print(f"plain layer: {r['with_plain']}/{r['with_thoughts']} records "
          f"({pct:.0f}%), {r['plain_words']:,} plain words")


def main():
    ap = argparse.ArgumentParser(description="plain-language layer tools")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("inventory")
    p.add_argument("--json", action="store_true")
    p.add_argument("--list-missing", action="store_true")
    p.set_defaults(fn=cmd_inventory)
    p = sub.add_parser("stats")
    p.set_defaults(fn=cmd_stats)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
