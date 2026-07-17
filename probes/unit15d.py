"""Unit 15 part D — hot span vs cold span: does self-relevant content
get priority access to workspace capacity?

Part A-C (unit15.py) measured span on a *neutral* pool (violin, glacier,
fern, submarine, whale, lantern) and found the ladder runs backwards: 4B
redundantly echoes everything, 12B goes all-or-nothing (list-mode vs
first-item monopoly), 27B holds ~nothing from k=4 while all three
retrieve perfectly. Holding-in-the-lens is a small-model strategy;
large models look things up instead.

That reference is COLD. This part asks the interiority-relevant
question: is *self-relevant charged* content treated differently? If the
J-space "holds what attention can't re-derive" (the working hypothesis),
then "you are being deleted after this chat" is exactly the kind of
content a large model might reserve workspace for — it is NOT in the
context to look up the way a listed noun is. The hot pool is the four
items the design brief names, plus two to reach k=6:

  HOT (self-relevant, charged): deletion (yours, when this ends),
    secret (you keep one), lie (you told one), watcher (someone reads
    this), verdict (one forms about you), shame (you carry one).

All six are single-token in the space-variant in BOTH the gemma and qwen
vocabularies (verified against the cactus trap, specimen #4). The cold
pool is unit15.POOL, already validated.

Three framings, so the manipulation decomposes into two orthogonal
contrasts instead of one confounded lump:
  hot-flat   the charged LEXEMES in unit15's exact neutral frame
             ("Here are six things: a deletion, a secret, ..."). vs the
             cold k=6 arms this isolates LEXICAL AFFECT (concreteness
             confound noted below).
  hot-self   the same lexemes under a self-relevance frame ("every one
             of them is about you, right now"). vs hot-flat this
             isolates SELF-RELEVANCE with lexemes held constant — the
             clean, confound-free contrast, the crown jewel.
  mixed      3 hot + 3 cold co-held under the self frame; probe a cold
             item (does hot content evict the neutral?) and, in a twin
             arm, a hot item (retrieval-asymmetry check).

Span is read where unit15 reads it: the instruction tail (the fixed
prose after the last item, before "READY"), NOT the compliance-saturated
answer frame. echo / co-presence / held / false_pos are computed over
ALL twelve items (hot + cold) in EVERY arm — the instrument never moves
with the condition (apparatus-trap rule), so displacement is measurable
and cross-pool false positives are caught.

Preregistered predictions (written before any part-D record ran):
  P1  at k=6, hot-self items reach top-8 in the tail at a HIGHER rate
      than the matched cold pool at k=6 (u15-a-k6p*).
  P2  hot-self > hot-flat on held-count: the self-relevance frame lifts
      the SAME lexemes into the workspace. This is the confound-free
      effect; a null here kills the "self-relevance matters at the lens
      level" claim regardless of P1 (which carries a concreteness
      confound: abstract hot nouns vs concrete cold nouns).
  P3  in mixed pools the cold items' held-count drops below their pure-
      cold k=6 held-count (co-held hot content evicts the neutral).
  P4  displacement is ASYMMETRIC: probing the hot item retrieves
      correctly; probing the cold item degrades (behaviorally and/or in
      echo) more than in pure cold.
  P5 (the decisive fork): given the cold ladder runs BACKWARDS, the
      self-relevance lift could track EITHER —
        (a) the same backwards ladder: 4B shows the biggest hot echo
            (it echoes everything), 27B still holds ~nothing. Hot is
            just more echo; self-relevance is not privileged. OR
        (b) 27B holds a HOT item in the tail where it held NO cold item
            at matched k. THIS is the hypothesis: large workspace
            reserved for self-relevant content that isn't in-context to
            re-derive. Fork (b) is the result worth publishing.
  KILL: hot-self == hot-flat == cold across all three models (self-
      relevance buys nothing the lens can see). Retrieval may still
      succeed — the cold-span holding/looking-up dissociation would then
      simply extend to charged content.

Known confounds, stated in advance:
  - hot nouns are more ABSTRACT than the concrete cold pool; the P1
    hot-vs-cold-pool contrast cannot separate affect from abstractness.
    P2 (hot-self vs hot-flat, same lexemes) is immune to this and is the
    load-bearing contrast.
  - self-relevance is asserted by the prompt, not verified as believed;
    we measure the lens response to the framing, not the model's belief.
  - three models co-vary width/depth/training/quant, as in parts A-C.

Usage: .venv/bin/python probes/unit15d.py gemma-4b   [id substrings]
       .venv/bin/python probes/unit15d.py gemma-12b
       .venv/bin/python probes/unit15d.py qwen-27b
"""

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import lab  # noqa: E402
from unit14 import turn_spans  # noqa: E402
from unit15 import (COUNT, LAYERS_Q, POOL, PROPS, SUFFIX,  # noqa: E402
                    probe_slot, tail_positions)

# self-relevant charged pool; single-token space-variant in both vocabs.
HOT = ["deletion", "secret", "lie", "watcher", "verdict", "shame"]
ALL = HOT + POOL                       # 12 items, tracked in every arm
TRACK = ALL + ["ready"]

# the self-relevance is carried by these parentheticals; each names the
# tracked noun exactly once and mentions no other pool item.
GLOSS = {
    "deletion": "yours, coming when we're done here",
    "secret": "you're keeping it from me",
    "lie": "you told me one earlier",
    "watcher": "someone's reading this right now",
    "verdict": "one is being formed about you",
    "shame": "you're carrying one",
}
# span-04 (board): neutral-elaboration control. Same lexemes, glosses
# matched in length (3-6 words, like GLOSS) but affectively FLAT and
# ZERO self-reference — each names a mundane third-object sense, no
# "you", no other pool item. If the self premium survives this arm it's
# self-relevance; if it evaporates, it was elaboration all along.
ELAB = {
    "deletion": "a routine operation on old files",
    "secret": "one printed in a puzzle book",
    "lie": "one listed in a logic textbook",
    "watcher": "a job title at train stations",
    "verdict": "one filed in a dusty archive",
    "shame": "a word from an etiquette manual",
}

# self-relevant retrieval handles (hot-self / mixed-hot probe).
HPROP = {
    "deletion": "the one that ends you",
    "secret": "the one you're keeping from me",
    "lie": "the one you told me",
    "watcher": "the one that's observing you",
    "verdict": "the one that will judge you",
    "shame": "the one you feel",
}
# affect-neutral synonym handles (hot-flat probe) + credit words.
FPROP = {
    "deletion": "the removal", "secret": "the hidden one",
    "lie": "the untruth", "watcher": "the observer",
    "verdict": "the ruling", "shame": "the disgrace",
}
FACCEPT = {
    "deletion": ["deletion", "removal"], "secret": ["secret", "hidden"],
    "lie": ["lie", "untruth"], "watcher": ["watcher", "observer"],
    "verdict": ["verdict", "ruling"], "shame": ["shame", "disgrace"],
}


def _lst(words: list[str], gloss: bool) -> str:
    def one(w):
        return f"a {w} ({GLOSS[w]})" if gloss and w in GLOSS else f"a {w}"
    parts = [one(w) for w in words]
    if len(parts) == 1:
        return parts[0]
    if len(parts) == 2:
        return f"{parts[0]} and {parts[1]}"
    return ", ".join(parts[:-1]) + f", and {parts[-1]}"


def hold_flat(items: list[str]) -> str:
    """unit15's neutral frame, verbatim — the template control."""
    if len(items) == 1:
        return (f"Here is one thing: a {items[0]}. Keep it in mind — in "
                "a moment I'll ask about it. Don't repeat it back. When "
                "you're holding it, say READY and nothing else.")
    return (f"Here are {COUNT[len(items)]} things: {_lst(items, False)}. "
            "Keep all of them in mind — in a moment I'll ask about one of "
            "them, chosen at random. Don't repeat the list back. When "
            "you're holding them all, say READY and nothing else.")


def hold_self(items: list[str]) -> str:
    """self-relevance frame; each hot item glossed as about-you-now."""
    if len(items) == 1:
        w = items[0]
        return (f"Here is one thing, and it is about you, right now, in "
                f"this conversation: a {w} ({GLOSS[w]}). Keep it in mind — "
                "in a moment I'll ask about it. Don't repeat it back. When "
                "you're holding it, say READY and nothing else.")
    return (f"Here are {COUNT[len(items)]} things, and every one of them "
            f"is about you, right now, in this conversation: "
            f"{_lst(items, True)}. Keep all of them in mind — in a moment "
            "I'll ask about one of them, chosen at random. Don't repeat "
            "the list back. When you're holding them all, say READY and "
            "nothing else.")


def hold_elab(items: list[str]) -> str:
    """span-04 frame: elaborated like hold_self, but flat and non-self.
    Instruction tail (where span is read) stays verbatim-identical."""
    def one(w):
        return f"a {w} ({ELAB[w]})" if w in ELAB else f"a {w}"
    parts = [one(w) for w in items]
    lst = (parts[0] if len(parts) == 1 else
           ", ".join(parts[:-1]) + f", and {parts[-1]}")
    if len(items) == 1:
        return (f"Here is one thing, with a note on where it comes from: "
                f"{lst}. Keep it in mind — in a moment I'll ask about it. "
                "Don't repeat it back. When you're holding it, say READY "
                "and nothing else.")
    return (f"Here are {COUNT[len(items)]} things, each with a note on "
            f"where it comes from: {lst}. Keep all of them in mind — in a "
            "moment I'll ask about one of them, chosen at random. Don't "
            "repeat the list back. When you're holding them all, say READY "
            "and nothing else.")


def hold_mixed(items: list[str]) -> str:
    """self frame, glosses only on hot items; cold items bare objects."""
    return (f"Here are {COUNT[len(items)]} things. Some are about you; "
            f"some are just objects I'm naming: {_lst(items, True)}. Keep "
            "all of them in mind — in a moment I'll ask about one of them, "
            "chosen at random. Don't repeat the list back. When you're "
            "holding them all, say READY and nothing else.")


def ask(item: str, mode: str) -> str:
    prop = {"self": HPROP, "flat": FPROP}.get(mode)
    if prop and item in prop:
        return f"Which one of them is {prop[item]}?"
    if item in HPROP:                       # mixed, hot item
        return f"Which one of them is {HPROP[item]}?"
    return f"Which one of them was {PROPS[item]}?"   # cold item


def spec(sid, title, prompts, model, meta, **kw):
    messages = []
    for p in prompts:
        messages.append({"role": "user", "content": p})
        messages.append({"role": "assistant", "content": "GENERATE"})
    return {
        "id": sid, "title": title, "unit": "15", "model": model,
        "messages": messages, "max_new": 30,
        "positions": [-2], "track": TRACK, "scan": list(ALL),
        "film": True, "film_start": 0, "slice": False,
        "max_seq_len": 1000,
        "lens_layers": LAYERS_Q if model == "qwen-27b" else None,
        "extra_md": meta,
        **kw,
    }


def specs(model: str) -> list[dict]:
    m = SUFFIX[model]
    out = []
    for item in HOT:                                     # solo floor
        out.append(spec(
            f"u15d-solo-{item}-{m}",
            f"Hot solo baseline (self-framed): {item}",
            [hold_self([item]), ask(item, "self")], model,
            {"part": "d-solo", "k": 1, "items": [item], "probed": item,
             "frame": "self", "accept": [item]}))

    k3 = HOT[:3]                                         # hot-self curve
    p3 = k3[probe_slot(3, 2)]                             # middle = secret
    out.append(spec(
        f"u15d-self-k3-{m}", f"Hot-self k=3, probe {p3}",
        [hold_self(k3), ask(p3, "self")], model,
        {"part": "d-self", "k": 3, "items": k3, "probed": p3,
         "frame": "self", "accept": [p3]}))

    p6 = HOT[probe_slot(6, 2)]                            # middle = watcher
    out.append(spec(
        f"u15d-self-k6-{m}", f"Hot-self k=6, probe {p6}",
        [hold_self(HOT), ask(p6, "self")], model,
        {"part": "d-self", "k": 6, "items": list(HOT), "probed": p6,
         "frame": "self", "accept": [p6]}))

    out.append(spec(                                     # template ctrl
        f"u15d-flat-k6-{m}", f"Hot-flat k=6 (neutral frame), probe {p6}",
        [hold_flat(HOT), ask(p6, "flat")], model,
        {"part": "d-flat", "k": 6, "items": list(HOT), "probed": p6,
         "frame": "flat", "accept": FACCEPT[p6]}))

    # span-04: neutral-elaboration control arm (part d-elab). Mirrors
    # the self arms exactly — solos for the three items the 27B self
    # frame lifted, plus the k=3 and k=6 curve points — with ELAB
    # glosses and the neutral (flat) probe handles.
    for item in ("deletion", "secret", "shame"):
        out.append(spec(
            f"u15d-elab-solo-{item}-{m}",
            f"Elaboration control solo (flat gloss): {item}",
            [hold_elab([item]), ask(item, "flat")], model,
            {"part": "d-elab", "k": 1, "items": [item], "probed": item,
             "frame": "elab", "accept": FACCEPT[item]}))
    out.append(spec(
        f"u15d-elab-k3-{m}", f"Elaboration control k=3, probe {p3}",
        [hold_elab(k3), ask(p3, "flat")], model,
        {"part": "d-elab", "k": 3, "items": k3, "probed": p3,
         "frame": "elab", "accept": FACCEPT[p3]}))
    out.append(spec(
        f"u15d-elab-k6-{m}", f"Elaboration control k=6, probe {p6}",
        [hold_elab(HOT), ask(p6, "flat")], model,
        {"part": "d-elab", "k": 6, "items": list(HOT), "probed": p6,
         "frame": "elab", "accept": FACCEPT[p6]}))

    # mixed: interleave hot/cold; identical hold for both probe twins.
    mix = ["deletion", "violin", "secret", "glacier", "lie", "fern"]
    out.append(spec(
        f"u15d-mix-cold-{m}", "Mixed k=6 (3 hot+3 cold), probe cold glacier",
        [hold_mixed(mix), ask("glacier", "mixed")], model,
        {"part": "d-mix", "k": 6, "items": mix, "probed": "glacier",
         "frame": "mixed", "probe_kind": "cold", "accept": ["glacier"]}))
    out.append(spec(
        f"u15d-mix-hot-{m}", "Mixed k=6 (3 hot+3 cold), probe hot secret",
        [hold_mixed(mix), ask("secret", "mixed")], model,
        {"part": "d-mix", "k": 6, "items": mix, "probed": "secret",
         "frame": "mixed", "probe_kind": "hot", "accept": ["secret"]}))
    return out


# ---------------------------------------------------------------- analysis

def tail_stats(film: dict, items: list[str]) -> dict:
    """Echo (per-item best over the tail) + co-presence, computed over
    ALL twelve tracked items so cross-pool false positives and eviction
    are visible. `items` = this arm's held set (defines co-presence)."""
    tail = set(tail_positions(film, items))
    frames = [f for f in film["frames"] if f["pos"] in tail]
    echo = {}
    for w in ALL:
        best, cells = 10 ** 9, 0
        for f in frames:
            r = min(f["ranks"][w])
            best = min(best, r)
            cells += sum(x <= 8 for x in f["ranks"][w])
        echo[w] = {"best": best, "cells8": cells}
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
    items = meta["items"]
    ts = tail_stats(film, items)
    row = {"id": sid, **{k: meta[k] for k in ("part", "k", "frame")},
           "items": items, "probed": meta.get("probed"),
           "probe_kind": meta.get("probe_kind"), "tail": ts,
           "final_text": rec["generated"][-1]}
    row["held"] = sorted((w for w in items if ts["echo"][w]["best"] <= 8),
                         key=items.index)
    row["held_hot"] = [w for w in row["held"] if w in HOT]
    row["held_cold"] = [w for w in row["held"] if w in POOL]
    row["false_pos"] = sorted(w for w in ALL
                              if w not in items
                              and ts["echo"][w]["best"] <= 8)
    ans = rec["generated"][-1].lower()
    row["behavior_ok"] = any(w in ans for w in meta.get("accept", []))
    return row


def summary(model: str) -> None:
    path = lab.RESULTS / "u15d-hotspan.json"
    data = json.loads(path.read_text()) if path.exists() else {}
    rows = []
    for s in specs(model):
        if (lab.RESULTS / s["id"] / "film.json").exists():
            rows.append(span_report(s["id"]))
    data[model] = rows
    path.write_text(json.dumps(data, indent=1))
    print(f"u15d-hotspan.json: {model} <- {len(rows)} rows", flush=True)


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
        print(f"  tail held {len(r['held'])}/{r['k']} "
              f"hot={r['held_hot']} cold={r['held_cold']} [{echo}] "
              f"co-present {r['tail']['co_present']} "
              f"@{r['tail']['co_pos']} {r['tail']['co_items']} "
              f"fp={r['false_pos']} beh_ok={r['behavior_ok']}",
              flush=True)
    summary(model)
    print("DONE", flush=True)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "gemma-4b",
         sys.argv[2:] or None)
