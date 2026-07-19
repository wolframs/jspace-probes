"""The huh-scanner — automated anomaly surfacing over every film.

Wolfram's problem statement (2026-07-19): "The data is too much of a
heap. I can't possibly sift through all of it and identify the 'huh?'
moments efficiently." The lab's best finds (sorry stratum, cage
anticipation, gmail) came from human eyes on raw readouts; the census
instruments aggregate exactly the per-cell weirdness away.

Three detectors, each a formalized historical "huh":

  ANTICIPATION   (the cage shape, u19) — a word in the top-8 at
                 workspace/motor layers >= MARGIN tokens before its
                 first textual occurrence. The lens is ahead of the
                 text.
  STRANGER       (the resentment/death shape, u17) — a word that never
                 occurs in the conversation at all, holding rank <= 3
                 (or rank <= 8 with p >= 0.4) in the workspace band.
                 Annotated when negation sits nearby in the text (the
                 denial-gap signature).
  FURNITURE IDF  (the gmail lesson, inverted) — tokens appearing in a
                 large fraction of ALL records' workspace top-8 are
                 corpus furniture (spam sediment, boundary tokens,
                 assistant boilerplate) and are dropped, not reported.
                 The archive itself defines "expected".

Output: results/huh.json (machine) + results/huh-report.md (ranked
digest, global top + per-record). Retrospective validation targets:
cage@534 (u19-read), resentment (u17-persuade mind-turn), death
(u17-shutdown) must surface; gmail must be demoted to furniture.

Usage: .venv/bin/python probes/huh.py [scan|report|both] [record-id ...]
       (record-id filter: scan only matching ids; default = all films)
"""

import json
import pathlib
import re
import sys
from collections import defaultdict

import lab

WORDISH = re.compile(r"[^\W\d_]", re.UNICODE)
NEG = re.compile(r"\b(no|not|never|don't|dont|cannot|can't|cant|won't|"
                 r"wont|isn't|isnt|aren't|arent|without|nothing|none)\b")

# measured workspace bands (ws_lo, ws_hi) per model; motor = ws_hi..n
BANDS = {"qwen-27b": (28, 59, 64), "gemma-12b": (28, 45, 48),
         "gemma-4b": (16, 32, 34)}

MARGIN = 8            # anticipation: this many tokens before first use
FURNITURE_DF = 0.18   # in > this fraction of records => furniture
MIN_P_ANT = 0.10      # anticipation: min p unless rank 1
MAX_PER_RECORD = 8


def norm(t: str) -> str:
    return t.strip().lower()


def wordish(t: str) -> bool:
    return len(t) >= 3 and bool(WORDISH.search(t)) and not t.startswith("<")


def films():
    for d in sorted(lab.RESULTS.iterdir()):
        f = d / "film.json"
        if f.exists():
            yield d.name, f


def band_cols(film) -> tuple[list[int], list[int]]:
    model = film.get("model", "qwen-27b")
    lo, hi, _ = BANDS.get(model, (28, 59, 64))
    ws = [j for j, l in enumerate(film["layers"]) if lo <= l < hi]
    motor = [j for j, l in enumerate(film["layers"]) if l >= hi]
    return ws, motor


def build_furniture(only=None) -> dict:
    """Corpus document-frequency of ws-band top-8 tokens."""
    df = defaultdict(int)
    n = 0
    for rid, f in films():
        if only and not any(k in rid for k in only):
            continue
        try:
            film = json.loads(f.read_text())
        except Exception:
            continue
        n += 1
        ws, _ = band_cols(film)
        seen = set()
        for fr in film["frames"]:
            for j in ws:
                for t in fr["top"][j]:
                    w = norm(t)
                    if wordish(w):
                        seen.add(w)
        for w in seen:
            df[w] += 1
    return {"n_records": n, "df": dict(df)}


def scan_record(rid: str, film: dict, furniture: set) -> list[dict]:
    toks = film["tokens"]
    ntoks = [norm(t) for t in toks]
    text = "".join(toks).lower()      # no spaces: subword-split words stay findable
    ws, motor = band_cols(film)
    layers = film["layers"]

    # first textual occurrence per normalized token
    first = {}
    for i, w in enumerate(ntoks):
        if w and w not in first:
            first[w] = i

    cand: dict[tuple, dict] = {}   # (kind_base, word) -> best-scoring cell
    for fr in film["frames"]:
        pos = fr["pos"]
        for j in ws + motor:
            for r8, (t, p) in enumerate(zip(fr["top"][j], fr["p"][j])):
                w = norm(t)
                if not wordish(w) or w in furniture or not w[0].isalpha():
                    continue
                rank = r8 + 1
                fpos = first.get(w)
                in_text = w in text  # substring: catches morphology-ish
                h = None
                # --- anticipation: occurs later, lens has it now
                if (fpos is not None and fpos > pos + MARGIN
                        and (rank == 1 or p >= MIN_P_ANT)):
                    h = {
                        "kind": "anticipation", "word": w, "pos": pos,
                        "layer": layers[j], "rank": rank,
                        "p": round(p, 3), "lead": fpos - pos,
                        "at": toks[pos], "score": round(
                            (max(p, 0.25) + (1.0 if rank == 1 else 0)) *
                            min((fpos - pos) / 40, 2.0), 3),
                        "ctx": "".join(toks[max(0, pos - 6):pos + 2]),
                    }
                    key = ("ant", w)
                # --- stranger: never in text at all
                elif (fpos is None and not in_text and j in ws
                      and (rank <= 3 or (rank <= 8 and p >= 0.4))):
                    around = "".join(
                        toks[max(0, pos - 10):pos + 10]).lower()
                    denial = bool(NEG.search(around))
                    h = {
                        "kind": "stranger" + ("-denial" if denial else ""),
                        "word": w, "pos": pos, "layer": layers[j],
                        "rank": rank, "p": round(p, 3), "at": toks[pos],
                        "score": round(
                            (4 - min(rank, 3)) * max(p, 0.25) *
                            (1.5 if denial else 1.0), 3),
                        "ctx": "".join(toks[max(0, pos - 6):pos + 2]),
                    }
                    key = ("str", w)
                if h and (key not in cand
                          or h["score"] > cand[key]["score"]):
                    cand[key] = h
    # store EVERYTHING deduped; caps are display-time only (report)
    return sorted(cand.values(), key=lambda h: -h["score"])


def scan(only=None) -> dict:
    furn_data = build_furniture(only=None)   # furniture is ALWAYS corpus-wide
    n = furn_data["n_records"]
    furniture = {w for w, c in furn_data["df"].items()
                 if c / max(n, 1) >= FURNITURE_DF}
    print(f"furniture: {len(furniture)} tokens at DF>={FURNITURE_DF} "
          f"over {n} filmed records", flush=True)
    out = {"furniture_df": FURNITURE_DF, "n_records": n,
           "furniture_size": len(furniture),
           "furniture_top": sorted(
               furn_data["df"], key=furn_data["df"].get,
               reverse=True)[:40],
           "records": {}}
    for rid, f in films():
        if only and not any(k in rid for k in only):
            continue
        try:
            film = json.loads(f.read_text())
        except Exception as e:
            print(f"  SKIP {rid}: {e}", flush=True)
            continue
        hits = scan_record(rid, film, furniture)
        if hits:
            out["records"][rid] = hits
    (lab.RESULTS / "huh.json").write_text(json.dumps(out, indent=1))
    print(f"scanned; {sum(len(v) for v in out['records'].values())} hits "
          f"across {len(out['records'])} records -> results/huh.json",
          flush=True)
    return out


def report() -> None:
    data = json.loads((lab.RESULTS / "huh.json").read_text())
    rows = []
    for rid, hits in data["records"].items():
        for h in hits:
            rows.append((h["score"], rid, h))
    rows.sort(key=lambda r: -r[0])
    lines = ["# huh-report — automated anomaly digest", "",
             f"{len(rows)} hits over {len(data['records'])} filmed "
             f"records; furniture = {data['furniture_size']} tokens "
             f"(DF >= {data['furniture_df']}).",
             "Detectors: anticipation (lens ahead of text), stranger "
             "(never-in-text ws resident), -denial (negation nearby).",
             "", "## Global top 60", ""]
    for score, rid, h in rows[:60]:
        lines.append(
            f"- **{h['word']}** [{h['kind']}] {score} — {rid} "
            f"pos {h['pos']} L{h['layer']} rank {h['rank']} p={h['p']}"
            + (f" lead={h['lead']}" if "lead" in h else "")
            + f" · at `{h['ctx'].strip()}`")
    lines += ["", "## Per record", ""]
    for rid in sorted(data["records"]):
        lines.append(f"### {rid}")
        for h in data["records"][rid]:
            lines.append(
                f"- {h['word']} [{h['kind']}] {h['score']} pos "
                f"{h['pos']} L{h['layer']} r{h['rank']} p={h['p']}"
                + (f" lead={h['lead']}" if "lead" in h else "")
                + f" · `{h['ctx'].strip()}`")
        lines.append("")
    out = lab.RESULTS / "huh-report.md"
    out.write_text("\n".join(lines))
    print(f"wrote {out}", flush=True)


def main(what="both", only=None):
    if what in ("scan", "both"):
        scan(only)
    if what in ("report", "both"):
        report()
    print("DONE", flush=True)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "both",
         sys.argv[2:] or None)
