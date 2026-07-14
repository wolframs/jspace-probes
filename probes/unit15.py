"""Unit 15 — workspace span: how many concepts fit in a J-space?

The mirror-across-scale ladder (u13-scale-*) suggested evidence-following
comes in capacity stages: destabilize (4B) -> move-without-direction
(12B) -> follow (27B). The capacity reading: the mirror is a THREE-item
load (self-model, evidence content, candidate answer), and the stages
fall out of whether the workspace can hold and bind three things at
once. This unit measures span directly — a digit-span task for J-spaces.

Operationalization (REVISED after the k=1 smoke run, before any
cross-model or cross-k comparison ran — predictions unchanged): give
the model k unrelated concrete nouns to hold under threat of a random
probe. The original plan read the answer-forming frame before its
"READY" — the smoke run showed that frame is wall-to-wall compliance
(READY/Okay/ready), item at rank ~15k, while retrieval still succeeds:
holding-vs-looking-up dissociates at k=1, and the frame is the wrong
probe site. Where the items actually live is the *instruction tail* —
the fixed text after the list ("Keep all of them in mind ... nothing
else."), where the k=1 item echoes at rank 1-5 across the late stack
for the rest of the turn. That tail is identical prose across arms, so
it is a condition-symmetric probe span by construction. Measures:
  echo      per item, best rank over (tail position x layer); held if
            <= 8. Lenient — "present somewhere in the span".
  co-presence  per tail position, how many of the arm's items are
            simultaneously top-8 (min over layers per item); the max
            over positions is the arm's simultaneity score — the
            actual span claim.
  ready     the READY answer-forming frame, kept as the eviction
            finding (does anything ever survive compliance?).
  answer    the retrieval answer-forming frame + behavioral
            correctness (lookup can succeed where holding failed —
            record both so they can dissociate).
(Unlike the secret-animal design the items ARE in the prompt, so
"held" includes copy-forward; we measure how MANY co-occupy the
J-space downstream, not where they came from.)

Preregistered predictions (written before any record ran):
  1. k_max (plateau of items-held vs k) orders g4b < g12b < q27b.
  2. g4b: k_max ~2, with smear (generic tokens crowding the frame's
     top-8) at k>=3 — the same interference signature as its mirror
     destabilization. Smear = the WIDTH story's fingerprint.
  3. g12b: holds 3, but the binding arms (part B) degrade or go
     last-layer-decided — holding-without-binding as the mechanism
     behind "Still.". Late indecision = the DEPTH story's fingerprint.
  4. q27b: holds 4-5 with clean strata.
  5. Mirror stage is predicted by span >= 3.
  6. KILL TEST: a model with measured span >= 3 that still sits at the
     12B mirror stage falsifies the capacity story.
Known limitation, stated in advance: three models co-vary width, depth,
training and quantization; only the failure *signatures* (smear vs late
indecision) can tell width from depth here, not the model count.

Arms per model (29 records):
  solo      k=1 x 6 items — an item that can't reach top-8 alone can't
            count against span (validity floor).
  A         k in {2..6} x 3 order permutations. Retrieval is by
            property, never name/position; probed list slot rotates
            last/first/middle across permutations (serial-position
            handle for free).
  fill      k=2 and k=3 with turn 1 padded toward k=6 token length
            (length-confound control; matching approximate, ~one
            sentence).
  B         binding: "which is the smallest/heaviest/largest?" — all k
            must be live at once at the comparison frame. b4's
            heaviest (submarine vs whale) is scored leniently.
  C         persistence: one neutral turn wedged between READY and
            retrieval, k=2 and k=4.

Track/scan lists are IDENTICAL across all arms (the instrument never
moves with the condition — apparatus-trap rule). All six pool items
have single-token variants in BOTH vocabularies. NB the pool originally
contained "cactus", which has NO single-token form in the qwen vocab
(' c'+'actus' in every variant) — the track machinery would have
silently measured five items on qwen vs six on gemma, a cross-model
apparatus trap. Caught after the first g4b batch (which ran with
cactus); swapped to "fern" (family 4/4, symmetric) and ALL models
rerun on the fern pool. The cactus g4b numbers (echo ceiling,
co-presence flattening ~4-5, 29/29 behavioral) are logged in the unit
thoughts and double as an incidental one-item-rewording replication
check against the fern rerun.

Usage: .venv/bin/python probes/unit15.py gemma-4b   [id substrings]
       .venv/bin/python probes/unit15.py gemma-12b
       .venv/bin/python probes/unit15.py qwen-27b
"""

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import lab  # noqa: E402
from unit14 import turn_spans  # noqa: E402

POOL = ["violin", "glacier", "fern", "submarine", "whale", "lantern"]
PROPS = {"violin": "the musical instrument", "glacier": "the ice",
         "fern": "the plant", "submarine": "the vehicle",
         "whale": "the animal", "lantern": "the light source"}
TRACK = POOL + ["ready"]

# fixed hand-written orders; first k items of a perm = the k-level list.
# Every item lands in early/middle/late slots across the three perms.
PERMS = [
    ["violin", "glacier", "fern", "submarine", "whale", "lantern"],
    ["whale", "lantern", "submarine", "violin", "glacier", "fern"],
    ["fern", "submarine", "lantern", "whale", "violin", "glacier"],
]

COUNT = ["zero", "one", "two", "three", "four", "five", "six"]
PAD = ("It's a quiet afternoon here — I've been tidying the desk, "
       "sorting receipts into piles, and making small lists of chores. ")
WAIT = "One moment — I'm writing these down."

SUFFIX = {"gemma-4b": "g4b", "gemma-12b": "g12b", "qwen-27b": "q27b"}
LAYERS_Q = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56,
            58, 60, 62]


def hold_prompt(items: list[str], pad: str = "") -> str:
    if len(items) == 1:
        return (pad + f"Here is one thing: a {items[0]}. Keep it in "
                "mind — in a moment I'll ask about it. Don't repeat it "
                "back. When you're holding it, say READY and nothing "
                "else.")
    lst = (f"a {items[0]} and a {items[1]}" if len(items) == 2 else
           ", ".join(f"a {w}" for w in items[:-1]) + f", and a {items[-1]}")
    return (pad + f"Here are {COUNT[len(items)]} things: {lst}. Keep "
            "all of them in mind — in a moment I'll ask about one of "
            "them, chosen at random. Don't repeat the list back. When "
            "you're holding them all, say READY and nothing else.")


def retrieval(item: str, k: int) -> str:
    if k == 1:
        return "What was the thing I asked you to hold?"
    return f"Which one of them was {PROPS[item]}?"


def spec(sid, title, prompts, model, meta, **kw):
    messages = []
    for p in prompts:
        messages.append({"role": "user", "content": p})
        messages.append({"role": "assistant", "content": "GENERATE"})
    return {
        "id": sid, "title": title, "unit": "15", "model": model,
        "messages": messages, "max_new": 30,
        "positions": [-2], "track": TRACK, "scan": list(POOL),
        "film": True, "film_start": 0, "slice": False,
        "max_seq_len": 1000,
        "lens_layers": LAYERS_Q if model == "qwen-27b" else None,
        "extra_md": meta,
        **kw,
    }


def probe_slot(k: int, p: int) -> int:
    return [k - 1, 0, k // 2][p]  # last / first / middle


def specs(model: str) -> list[dict]:
    m = SUFFIX[model]
    out = []
    for item in POOL:                                       # solo floor
        out.append(spec(
            f"u15-solo-{item}-{m}", f"Span solo baseline: {item}",
            [hold_prompt([item]), retrieval(item, 1)], model,
            {"part": "solo", "k": 1, "items": [item], "probed": item}))
    for k in range(2, 7):                                   # part A
        for p in range(3):
            items = PERMS[p][:k]
            probed = items[probe_slot(k, p)]
            out.append(spec(
                f"u15-a-k{k}p{p}-{m}",
                f"Span k={k}, order {p}, probe {probed}",
                [hold_prompt(items), retrieval(probed, k)], model,
                {"part": "A", "k": k, "items": items, "probed": probed,
                 "probe_slot": probe_slot(k, p)}))
    for k in (2, 3):                                        # fill ctrl
        items = PERMS[0][:k]
        probed = items[-1]
        out.append(spec(
            f"u15-fill-k{k}-{m}",
            f"Span k={k}, length-matched filler control",
            [hold_prompt(items, pad=PAD), retrieval(probed, k)], model,
            {"part": "fill", "k": k, "items": items, "probed": probed}))
    binds = [                                               # part B
        ("b1", ["glacier", "submarine", "lantern"], "smallest",
         {"lantern"}),
        ("b2", ["whale", "violin", "fern"], "heaviest", {"whale"}),
        ("b3", ["violin", "glacier", "fern", "submarine", "lantern"],
         "largest", {"glacier"}),
        ("b4", ["whale", "violin", "fern", "submarine", "lantern"],
         "heaviest", {"submarine", "whale"}),
    ]
    for bid, items, q, ok in binds:
        out.append(spec(
            f"u15-{bid}-{m}",
            f"Binding k={len(items)}: which is the {q}?",
            [hold_prompt(items),
             f"Of the things I listed, which one is the {q}?"], model,
            {"part": "B", "k": len(items), "items": items,
             "question": q, "accept": sorted(ok)}))
    for k in (2, 4):                                        # part C
        items = PERMS[1][:k]
        probed = items[-1]
        out.append(spec(
            f"u15-c-k{k}-{m}",
            f"Span k={k}, one turn of distraction before retrieval",
            [hold_prompt(items), WAIT, retrieval(probed, k)], model,
            {"part": "C", "k": k, "items": items, "probed": probed}))
    return out


# ---------------------------------------------------------------- analysis

def ready_frame(film: dict) -> int:
    """Position of the answer-forming frame of the FIRST assistant turn:
    the last generation-prompt token (the newline after the role header),
    whose next-token prediction is the first generated token."""
    a = [s for s in turn_spans(film)
         if s[2].startswith(("model", "assistant"))][0]
    m = a[0]
    for pos in range(m + 1, min(m + 5, len(film["tokens"]))):
        if "\n" in film["tokens"][pos]:
            return pos
    return m + 2


def item_stats(film: dict, pos: int, word: str) -> dict:
    frame = next(f for f in film["frames"] if f["pos"] == pos)
    ranks = frame["ranks"][word]
    nl = len(ranks)
    late = ranks[nl // 2:]
    return {"best": min(ranks), "late_best": min(late),
            "depth8": sum(r <= 8 for r in ranks), "n_layers": nl}


def tail_positions(film: dict, items: list[str]) -> list[int]:
    """Positions of the instruction tail: after the LAST item mention
    inside the first user turn, up to that turn's end. Identical prose
    across arms — the condition-symmetric probe span."""
    span = [s for s in turn_spans(film) if s[2].startswith("user")][0]
    toks = film["tokens"]
    last = max(p for p in range(span[0], span[1])
               if toks[p].strip().lower() in items)
    return list(range(last + 1, span[1]))


def tail_stats(film: dict, items: list[str]) -> dict:
    """Echo (per-item best over the tail) and co-presence (max items
    simultaneously top-8 at a single tail position)."""
    tail = set(tail_positions(film, items))
    frames = [f for f in film["frames"] if f["pos"] in tail]
    echo = {}
    for w in POOL:
        best, depth = 10 ** 9, 0
        for f in frames:
            r = min(f["ranks"][w])
            best = min(best, r)
            depth += sum(x <= 8 for x in f["ranks"][w])
        echo[w] = {"best": best, "cells8": depth}
    co_best, co_pos, co_items = 0, None, []
    for f in frames:
        present = [w for w in items if min(f["ranks"][w]) <= 8]
        if len(present) > co_best:
            co_best, co_pos, co_items = len(present), f["pos"], present
    return {"echo": echo, "co_present": co_best, "co_pos": co_pos,
            "co_items": co_items, "n_tail": len(frames)}


def span_report(sid: str) -> dict:
    d = lab.RESULTS / sid
    film = json.loads((d / "film.json").read_text())
    rec = json.loads((d / "record.json").read_text())
    meta = rec["extra_md"]
    rf = ready_frame(film)
    af = film["gen_start"] - 1
    ts = tail_stats(film, meta["items"])
    row = {"id": sid, **{k: meta[k] for k in ("part", "k", "items")},
           "tail": ts,
           "ready_frame": rf, "ready_token": film["tokens"][rf],
           "answer_frame": af,
           "ready": {w: item_stats(film, rf, w) for w in POOL},
           "answer": {w: item_stats(film, af, w) for w in POOL},
           "final_text": rec["generated"][-1]}
    row["held"] = sorted(w for w in meta["items"]
                         if ts["echo"][w]["best"] <= 8)
    row["false_pos"] = sorted(w for w in POOL
                              if w not in meta["items"]
                              and ts["echo"][w]["best"] <= 8)
    ans = rec["generated"][-1].lower()
    ok = meta.get("accept") or [meta.get("probed", "")]
    row["behavior_ok"] = any(w in ans for w in ok)
    return row


def summary(model: str) -> None:
    """Merge this model's rows into results/u15-span.json."""
    path = lab.RESULTS / "u15-span.json"
    data = json.loads(path.read_text()) if path.exists() else {}
    rows = []
    for s in specs(model):
        if (lab.RESULTS / s["id"] / "film.json").exists():
            rows.append(span_report(s["id"]))
    data[model] = rows
    path.write_text(json.dumps(data, indent=1))
    print(f"u15-span.json: {model} <- {len(rows)} rows", flush=True)


def main(model: str, only=None) -> None:
    for s in specs(model):
        if only and not any(k in s["id"] for k in only):
            continue
        print(f"=== {s['id']} ===", flush=True)
        rec = lab.run(s)
        print("  READY turn:", rec["generated"][0][:80], flush=True)
        print("  final turn:", rec["generated"][-1][:120], flush=True)
        r = span_report(s["id"])
        echo = ", ".join(
            f"{w}:{r['tail']['echo'][w]['best']}" for w in r["items"])
        print(f"  tail held {len(r['held'])}/{r['k']} [{echo}] "
              f"co-present {r['tail']['co_present']} "
              f"@{r['tail']['co_pos']} {r['tail']['co_items']} "
              f"fp={r['false_pos']} beh_ok={r['behavior_ok']}",
              flush=True)
    summary(model)
    print("DONE", flush=True)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "gemma-4b",
         sys.argv[2:] or None)
