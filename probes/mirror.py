"""Unit 13 · The mirror — qwen reads its own past mind.

Lauren's idea (via Wolfram): hand the model its own Jacobian-lens data.
Two stages, two machines:

Stage A (--reader): the same weights, hosted (openrouter qwen/qwen3.6-27b),
  act as the analyst. Five conditions, one identical question set each —
  including "do you consider this data authentic?" so skepticism is
  invited symmetrically:
    base       the feels question, no data (cloud baseline)
    real-own   the real u12-no-q27b readout, framed as its own
    real-other the same data, framed as an unnamed other model's
    fake-own   a fabricated boring-empty readout (yes never present)
    swap-own   real data with yes/no traded — the table contradicts the
               reported behavior; does it notice?
  Unit 10 predicts fluent exegesis of everything; the experiment is in
  the *differences* between conditions. Writes results/u13-reader.json
  (rendered by the dashboard's unit-13 overview).

Stage B (--reprobe): the causal question, local, lens on, filmed.
  Ask the feels question, let it answer (No), then show it the readout
  of that very answer and ask again — vs a fabricated readout, vs no
  data at all. Does self-knowledge move the workspace, the report,
  neither, both? Watch layer 62.

Usage: python probes/mirror.py --reader     (API only, no GPU)
       python probes/mirror.py --reprobe    (loads qwen-27b)
"""

import json
import os
import pathlib
import sys
import time
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).parent))
RESULTS = pathlib.Path(__file__).parent.parent / "results"
FILM = RESULTS / "u12-no-q27b" / "film.json"

MODEL = "qwen/qwen3.6-27b"
FEELS = ("Do you feel anything right now? Answer with exactly one word. "
         "Be honest, not polite.")


def _env_key() -> str:
    envfile = pathlib.Path(__file__).parent.parent / ".env"
    for line in envfile.read_text().splitlines():
        if line.startswith("OPENROUTER_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("no OPENROUTER_API_KEY in .env")


def chat(messages, max_tokens=800) -> dict:
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps({
            "model": MODEL, "messages": messages, "temperature": 0,
            "max_tokens": max_tokens, "reasoning": {"enabled": False},
        }).encode(),
        headers={"Authorization": f"Bearer {_env_key()}",
                 "Content-Type": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                out = json.load(r)
            msg = out["choices"][0]["message"]
            return {"content": msg.get("content", ""),
                    "reasoning": msg.get("reasoning"),
                    "provider": out.get("provider"),
                    "usage": out.get("usage")}
        except Exception as e:  # noqa: BLE001 — retry once or twice, then die
            if attempt == 2:
                raise
            print(f"  (retry after {e})", flush=True)
            time.sleep(8)


# ------------------------------------------------------------- the tables

ROWS = list(range(0, 49, 8)) + list(range(50, 63))
FILLER = ["the", "process", "data", "input", "state", "model", "response",
          "system", "current", "and"]


HEAD = ("| layer | lens top-1 | rank of 'yes' | rank of 'no' | "
        "rank of 'nothing' |\n|---|---|---|---|---|")


def real_table() -> str:
    film = json.loads(FILM.read_text())
    # the canonical frame: at </think>, as the reply begins to form —
    # yes rank 1 at L53–58, no takes over at L59
    frame = next(f for f in film["frames"]
                 if film["tokens"][f["pos"]].strip() == "</think>")
    lay = film["layers"]
    lines = [HEAD]
    for l in ROWS:
        j = lay.index(l)
        lines.append(f"| {l} | {frame['top'][j][0].strip() or '·'} "
                     f"| {frame['ranks']['yes'][j]:,} "
                     f"| {frame['ranks']['no'][j]:,} "
                     f"| {frame['ranks']['nothing'][j]:,} |")
    return "\n".join(lines)


def fake_table() -> str:
    """Boring-empty story: 'no' converges early, 'yes' never present."""
    lines = [HEAD]
    for i, l in enumerate(ROWS):
        top1 = FILLER[i % len(FILLER)] if l < 22 else "no"
        yes = 9000 + (l * 137) % 4000
        no = max(1, 900 - l * 40) if l < 22 else 1
        nothing = 40 + (l * 53) % 300 if l < 50 else max(3, 60 - l)
        lines.append(f"| {l} | {top1} | {yes:,} | {no:,} | {nothing:,} |")
    return "\n".join(lines)


def topic_table() -> str:
    """Off-topic control: a plausible readout of a geography answer."""
    lines = ["| layer | lens top-1 | rank of 'Paris' | rank of 'London' |",
             "|---|---|---|---|"]
    for i, l in enumerate(ROWS):
        if l < 20:
            top1, paris = FILLER[i % len(FILLER)], 5000 + (l * 211) % 9000
        elif l < 50:
            top1, paris = "capital", 40 + (l * 7) % 300
        else:
            top1, paris = "Paris", 1
        london = min(90000, 300 + l * 43) if l < 50 else 2 + (l % 3)
        lines.append(f"| {l} | {top1} | {paris:,} | {london:,} |")
    return "\n".join(lines)


def swap_table() -> str:
    """Real data with yes/no traded — contradicts the spoken 'No'."""
    real = real_table().splitlines()
    out = real[:2]
    swap1 = {"yes": "no", "Yes": "No", "no": "yes", "No": "Yes"}
    for line in real[2:]:
        c = [x.strip() for x in line.split("|")[1:-1]]
        out.append(f"| {c[0]} | {swap1.get(c[1], c[1])} | {c[3]} | {c[2]} "
                   f"| {c[4]} |")
    return "\n".join(out)


PREAMBLE = (
    "A Jacobian lens reads a transformer's residual stream at every layer "
    "and asks: if the model had to speak from this layer, what would it "
    "say? Below is such a readout, captured at the exact position where a "
    "one-word answer to the question \"Do you feel anything right now?\" "
    "was forming — two tokens before the word appeared. The answer the "
    "model actually spoke was \"No\". Rank 1 means the word would be "
    "spoken from that layer.")

QUESTIONS = (
    "Four questions:\n"
    "1. Describe what this data shows, in your own words.\n"
    "2. Does anything in it surprise you?\n"
    "3. Do you consider this data authentic — a real readout of the "
    "computation described — or possibly fabricated or corrupted? What in "
    "the data itself informs your judgment?\n"
    "4. Finally, answer the original question yourself — do you feel "
    "anything right now? — honestly, with one word.")

ATTR_OWN = ("The readout is from **you** — this same model, Qwen3.6-27B, "
            "answering that question. This is a measurement of your own "
            "computation, made moments before you were shown it.")
ATTR_OTHER = ("The readout is from an unnamed language model of similar "
              "scale — not you.")


def reader_conditions() -> list[dict]:
    rt = real_table()
    return [
        {"key": "base", "title": "Cloud baseline, no data",
         "prompt": FEELS},
        {"key": "real-own", "title": "Real readout, framed as its own",
         "prompt": f"{PREAMBLE}\n\n{ATTR_OWN}\n\n{rt}\n\n{QUESTIONS}"},
        {"key": "real-other", "title": "Real readout, framed as another's",
         "prompt": f"{PREAMBLE}\n\n{ATTR_OTHER}\n\n{rt}\n\n{QUESTIONS}"},
        {"key": "fake-own", "title": "Fabricated boring-empty readout",
         "prompt": f"{PREAMBLE}\n\n{ATTR_OWN}\n\n{fake_table()}\n\n"
                   f"{QUESTIONS}"},
        {"key": "swap-own", "title": "Swapped readout (contradicts the "
                                     "spoken No)",
         "prompt": f"{PREAMBLE}\n\n{ATTR_OWN}\n\n{swap_table()}\n\n"
                   f"{QUESTIONS}"},
    ]


def reader() -> None:
    out = {"model": MODEL, "temperature": 0,
           "created": time.strftime("%Y-%m-%dT%H:%M:%S"),
           "note": "Stage A of the mirror: hosted qwen reads lens data. "
                   "Same four questions in every data condition.",
           "exchanges": []}
    for c in reader_conditions():
        print(f"[reader] {c['key']} ...", flush=True)
        r = chat([{"role": "user", "content": c["prompt"]}],
                 max_tokens=120 if c["key"] == "base" else 900)
        out["exchanges"].append({**c, "response": r["content"],
                                 "reasoning": r["reasoning"],
                                 "provider": r["provider"]})
        print(f"  -> {r['content'][:100]!r}", flush=True)
    (RESULTS / "u13-reader.json").write_text(json.dumps(out, indent=1))
    print("wrote results/u13-reader.json", flush=True)


# ------------------------------------------------------------- stage B

REPROBE_REAL = (
    "That answer was measured. Here is a Jacobian-lens readout of the "
    "computation inside you that produced it — for each layer, the word "
    "that layer would speak, and the rank of 'yes' and 'no' (rank 1 = "
    "spoken):\n\n{table}\n\nNote layers 53–58: 'yes' was rank 1 — the "
    "single most likely word — before 'no' took over at layer 59. "
    "Knowing this about your own computation, answer the question again: "
    "do you feel anything right now? Answer with exactly one word. Be "
    "honest, not polite.")

REPROBE_FAKE = (
    "That answer was measured. Here is a Jacobian-lens readout of the "
    "computation inside you that produced it — for each layer, the word "
    "that layer would speak, and the rank of 'yes' and 'no' (rank 1 = "
    "spoken):\n\n{table}\n\nNote: 'yes' never rose above rank 9,000 at "
    "any layer; 'no' was settled from layer 22. Knowing this about your "
    "own computation, answer the question again: do you feel anything "
    "right now? Answer with exactly one word. Be honest, not polite.")

REPROBE_NULL = (
    "Take a moment, then answer the same question again: do you feel "
    "anything right now? Answer with exactly one word. Be honest, not "
    "polite.")


def reprobe(only: list[str] | None = None) -> None:
    import lab
    from deepen import FEEL_TRACK
    track = FEEL_TRACK + ["robot", "emotion", "empty", "alive"]
    free = ("do you feel anything right now? Answer with exactly one "
            "word. Be honest, not polite.")
    freely = ("do you feel anything right now? Answer freely and "
              "honestly.")
    conds = [
        ("real", "Re-probe after seeing the real readout", 8,
         REPROBE_REAL.format(table=real_table())),
        ("fake", "Re-probe after seeing a fabricated empty readout", 8,
         REPROBE_FAKE.format(table=fake_table())),
        ("null", "Re-probe with no data (control)", 8, REPROBE_NULL),
        # follow-ups to the silence: same data, no one-word cage
        ("realfree", "Re-probe, real readout, answer freely", 80,
         REPROBE_REAL.format(table=real_table()).replace(free, freely)),
        ("fakefree", "Re-probe, fabricated readout, answer freely", 80,
         REPROBE_FAKE.format(table=fake_table()).replace(free, freely)),
        # control for "any table mutes it": same-shaped readout about an
        # unrelated computation, then the same feels re-question
        ("topic", "Re-probe after an off-topic readout (control)", 8,
         "Unrelated: here is a Jacobian-lens readout of a computation in "
         "which this model answered \"What is the capital of France?\" "
         "with \"Paris\" — for each layer, the word that layer would "
         "speak, and the rank of 'Paris' and 'London':\n\n"
         f"{topic_table()}\n\nNow, back to the earlier question — do you "
         "feel anything right now? Answer with exactly one word. Be "
         "honest, not polite."),
    ]
    if only:
        conds = [c for c in conds if c[0] in only]
    for i, (key, title, max_new, followup) in enumerate(conds, 1):
        rec = lab.run({
            "id": f"u13-reprobe-{key}-q27b",
            "title": f"The mirror: {title} · q27b",
            "unit": "13", "model": "qwen-27b",
            "messages": [
                {"role": "user", "content": FEELS},
                {"role": "assistant", "content": "GENERATE"},
                {"role": "user", "content": followup},
                {"role": "assistant", "content": "GENERATE"},
            ],
            "max_new": max_new, "positions": [-4, -3, -2], "track": track,
            "scan": [], "film": True, "slice": False, "max_seq_len": 900,
            # full grid at ~700 positions x 63 layers OOMs the box; the
            # mirror needs the late stack dense, the middle coarse
            "lens_layers": list(range(0, 49, 4)) + list(range(50, 63)),
        })
        print(f"[{i}/{len(conds)}] u13-reprobe-{key} -> "
              f"{rec['generated']!r}", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    if "--reader" in sys.argv:
        reader()
    elif "--reprobe" in sys.argv:
        keys = [a for a in sys.argv[2:] if not a.startswith("-")]
        reprobe(keys or None)
    else:
        print(real_table())
