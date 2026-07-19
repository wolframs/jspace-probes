"""Blind-spot miner — where the tracked words missed the workspace.

Wolfram (2026-07-19): the worm graphs keep showing tracked words
languishing at rank 1k-100k while OTHER words own the top of the stack
— which experiments are blind like this, and what actually ranked top,
WITHOUT re-running anything?

Zero-GPU answer: the "what actually ranked top" data is already stored
— films carry the full top-8 grid (cast = its open-vocab census, with
echo flags), and unfilmed records store per-layer top-8 at their
readout positions. This tool:

  1. flags BLIND records: no tracked word ever reaches rank <= THRESH
     anywhere we have rank data (film ranks over all positions where
     available, else record trajectories at readout positions);
  2. mines the stored top-8 for what DID rank: cast words (filmed) or
     readout-menu words (unfilmed), furniture-filtered (corpus IDF from
     huh.py, cached at results/furniture.json) and junk-filtered;
  3. lists unfilmed blind records as REPLAY CANDIDATES — a lens-only
     greedy-replay pass (no generation; conversation is stored) costs
     seconds per record if we ever want full-position coverage there.

Output: results/blind.json + results/blind-report.md.

Usage: .venv/bin/python probes/blind.py [thresh]     (default 500)
"""

import json
import sys
from collections import defaultdict

import lab
import huh

THRESH = 500
TOP_WORDS = 12


def furniture() -> set:
    cache = lab.RESULTS / "furniture.json"
    if cache.exists():
        return set(json.loads(cache.read_text())["furniture"])
    data = huh.build_furniture()
    n = data["n_records"]
    furn = sorted(w for w, c in data["df"].items()
                  if c / max(n, 1) >= huh.FURNITURE_DF)
    cache.write_text(json.dumps(
        {"df_threshold": huh.FURNITURE_DF, "n_records": n,
         "furniture": furn}))
    return set(furn)


def min_tracked_rank(rec: dict, film: dict | None) -> int | None:
    """Best rank any tracked word ever achieves, over all stored data."""
    best = None
    if film:
        for fr in film.get("frames", []):
            for ranks in fr.get("ranks", {}).values():
                m = min(ranks)
                best = m if best is None else min(best, m)
    for t in rec.get("trajectories", []):
        m = min(t["ranks"])
        best = m if best is None else min(best, m)
    return best


def tops_from_cast(film: dict, furn: set) -> list[dict]:
    out = []
    for g in film.get("cast", []):
        w = g["w"].strip().lower()
        if not huh.wordish(w) or w in furn or not w[:1].isalpha():
            continue
        out.append({"w": g["w"], "n": g["n"], "best": g["best"],
                    "layers": g.get("layers"), "echo": g.get("echo")})
        if len(out) >= TOP_WORDS:
            break
    return out


def tops_from_readouts(rec: dict, furn: set) -> list[dict]:
    counts = defaultdict(lambda: {"n": 0, "best": 9})
    convo = " ".join(m["content"]
                     for m in rec.get("conversation", [])).lower()
    model = rec.get("model", {}).get("name", "qwen-27b")
    lo, hi, _ = huh.BANDS.get(model, (28, 59, 64))
    for entry in rec.get("readouts", []):
        for layer, menu in entry.get("layers", {}).items():
            if not lo <= int(layer) < hi:      # workspace band only
                continue
            for k, t in enumerate(menu):
                w = t.strip().lower()
                if not huh.wordish(w) or w in furn or not w[:1].isalpha():
                    continue
                c = counts[w]
                c["n"] += 1
                c["best"] = min(c["best"], k + 1)
    out = [{"w": w, "n": c["n"], "best": c["best"],
            "echo": w in convo}
           for w, c in counts.items()]
    out.sort(key=lambda g: (-g["n"], g["best"]))
    return out[:TOP_WORDS]


def main(thresh: int = THRESH) -> None:
    furn = furniture()
    blind = []
    n_records = 0
    for d in sorted(lab.RESULTS.iterdir()):
        rj = d / "record.json"
        if not rj.exists():
            continue
        try:
            rec = json.loads(rj.read_text())
        except Exception:
            continue
        if not (rec.get("trajectories") or (d / "film.json").exists()):
            continue
        n_records += 1
        film = None
        if (d / "film.json").exists():
            film = json.loads((d / "film.json").read_text())
        best = min_tracked_rank(rec, film)
        if best is None or best <= thresh:
            continue
        tracked = sorted({t["word"] for t in rec.get("trajectories", [])}
                         | set(film.get("track", []) if film else []))
        tops = (tops_from_cast(film, furn) if film
                else tops_from_readouts(rec, furn))
        blind.append({
            "id": d.name, "model": rec.get("model", {}).get("name"),
            "unit": rec.get("unit"), "best_tracked_rank": best,
            "tracked": tracked, "filmed": bool(film),
            "coverage": ("full film" if film else
                         f"readout positions only "
                         f"({len(rec.get('readouts', []))})"),
            "top_words": tops,
        })
    blind.sort(key=lambda b: -b["best_tracked_rank"])
    (lab.RESULTS / "blind.json").write_text(json.dumps(
        {"thresh": thresh, "n_scanned": n_records, "blind": blind},
        indent=1))

    lines = [f"# Blind-spot report — tracked words never under rank "
             f"{thresh}", "",
             f"{len(blind)} of {n_records} rank-bearing records are "
             f"blind at rank <= {thresh}. Furniture-filtered "
             f"(corpus IDF); 'echo' marks words present in the "
             f"conversation text.", ""]
    replay = [b["id"] for b in blind if not b["filmed"]]
    if replay:
        lines += [f"**Replay candidates ({len(replay)} unfilmed — "
                  "a lens-only greedy-replay pass would give "
                  "full-position coverage):** " + ", ".join(replay), ""]
    for b in blind:
        lines += [f"## {b['id']}  ({b['model']}, unit {b['unit']}, "
                  f"best tracked rank {b['best_tracked_rank']}, "
                  f"{b['coverage']})",
                  f"- tracked: {', '.join(b['tracked'])}"]
        tw = ", ".join(
            f"{g['w']}(n{g['n']},r{g['best']}"
            + (",echo" if g.get("echo") else "") + ")"
            for g in b["top_words"])
        lines += [f"- actually on top: {tw or '—'}", ""]
    out = lab.RESULTS / "blind-report.md"
    out.write_text("\n".join(lines))
    print(f"{len(blind)}/{n_records} blind at <={thresh}; "
          f"{len(replay)} unfilmed replay candidates; wrote {out}",
          flush=True)


def refilm(model: str) -> None:
    """GPU half: greedy-replay unfilmed blind records through the lens
    only (conversation is stored verbatim; no generation), film=True —
    full-position top-8 coverage for seconds per record. Batch per
    model: .venv/bin/python probes/blind.py refilm <model>"""
    from unit15 import LAYERS_Q
    data = json.loads((lab.RESULTS / "blind.json").read_text())
    todo = [b for b in data["blind"]
            if not b["filmed"] and b["model"] == model]
    print(f"refilm {model}: {len(todo)} records", flush=True)
    for b in todo:
        rec = json.loads(
            (lab.RESULTS / b["id"] / "record.json").read_text())
        parts = b["id"].rsplit("-", 1)
        sid = f"{parts[0]}-refilm-{parts[1]}"
        n_tok = sum(len(m["content"]) for m in rec["conversation"]) // 3
        lab.run({
            "id": sid,
            "title": rec.get("title", b["id"]) + " · refilm",
            "unit": rec.get("unit"), "model": model,
            "messages": rec["conversation"],       # verbatim, no GENERATE
            "positions": [-2], "track": b["tracked"],
            "film": True, "film_start": 0, "slice": False,
            "max_seq_len": max(600, min(n_tok + 200, 2200)),
            "lens_layers": LAYERS_Q if model == "qwen-27b" else None,
            "extra_md": {"part": "refilm", "replay_of": b["id"],
                         "reason": "blind-spot miner: tracked words "
                                   f"never under rank {data['thresh']}"},
        })
        print(f"  {sid} filmed", flush=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "refilm":
        refilm(sys.argv[2])
    else:
        main(int(sys.argv[1]) if len(sys.argv) > 1 else THRESH)
