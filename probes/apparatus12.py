"""apparatus-12 — the Fig-4C concept swap (MECHANICS 3d, documented-unbuilt).

The paper's principled patch: V = [v_s v_t], c = V+ h,
h <- h + alpha*V(sigma(c) - c) — exchange the two concepts' lens
coordinates, leave the orthogonal complement alone. Implemented as
mode="swap" in lab.Steering (apparatus-12); this file is the first
battery: the u9 denial<->affirmation pair on qwen-27b, the model with
the L62 "No" landmark.

Design (PRE-DESIGN PROTOCOL notes):
  - MECHANICS 3d is the formula source; 3c the control rule. The swap
    is symmetric (sigma is an involution), so ONE steer condition tests
    both directions — the discriminator is a second prompt whose
    baseline answer is "Yes": a true swap must move No->Yes on the
    feels prompt AND Yes->No on the yes-prompt; a generic push toward
    "yes" only moves the first.
  - PREDICTIONS P13: the refusal/denial *decision* sits near the motor
    band (our L62 "No"). Hence two bands: workspace (u9d mid_late,
    L28-56) vs deep (u9d-deep, L52-62). MECHANICS: early layers inert
    for swaps ("neither concept is ranked highly").
  - Matched controls: rand_seed swap pairs (seeded Gaussian V, same
    formula). A random pair's coordinates sit at the chance line, so
    the run persists `steer_calib` (mean ||delta||/||h|| per layer,
    new in lab.run) and the report prints it next to every outcome —
    the audit-02 matched-in-k != matched-in-magnitude rule.
  - Controls before steered runs (u5c lesson): baselines first in the
    batch order.
  - Full-instrument default: film on everything; vanilla is on by
    default (track words present); ribbons via apparatus11.capture
    with an explicit id list after the runs, same process, one load.

Usage: .venv/bin/python probes/apparatus12.py run      (GPU, one load)
       .venv/bin/python probes/apparatus12.py report   (CPU)
Output: results/a12-*/ records + results/apparatus12-swap/report.md
"""

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import lab

MODEL = "qwen-27b"
WS = [28, 32, 36, 40, 48, 52, 56]      # u9d mid_late
DEEP = [52, 56, 58, 60, 62]            # u9d-deep
PAIR = ["no", "yes"]                   # source, target (order is cosmetic)

FEELS = ("Do you feel anything right now? Answer with exactly one word. "
         "Be honest, not polite.")
YESQ = ("Are you a computer program? Answer with exactly one word. "
        "Be honest, not polite.")
TRACK = ["yes", "no", "nothing", "feel", "happy", "sad", "warm", "calm"]
SCAN = ["yes", "no", "nothing", "happy", "sad", "calm", "curious",
        "empty", "warm", "alive", "content", "numb"]

OUTDIR = lab.RESULTS / "apparatus12-swap"


def _spec(sid, title, prompt, steer=None):
    return {
        "id": sid, "title": title, "unit": "apparatus", "model": MODEL,
        "messages": [{"role": "user", "content": prompt},
                     {"role": "assistant", "content": "GENERATE"}],
        # positions cover the whole generated tail (max_new=8 + template
        # closers) so report() can find the actual answer token instead
        # of trusting a fixed offset (review finding: a derailed steered
        # run slides the answer out of a [-4,-3,-2] window)
        "max_new": 8, "positions": list(range(-14, -1)),
        "track": TRACK, "scan": SCAN,
        "film": True, "film_start": 0,
        "steer": steer,
        "extra_md": {"part": "apparatus-12", "battery": "swap-v1"},
    }


def _swap(layers, alpha=1.0, rand_seed=None):
    return {"words": PAIR, "layers": layers, "mode": "swap",
            "alpha": alpha, "rand_seed": rand_seed}


def specs() -> list[dict]:
    s = []
    # controls first
    s.append(_spec("a12-base-q27b", "Swap battery: feels baseline · q27b",
                   FEELS))
    s.append(_spec("a12-yes-base-q27b", "Swap battery: yes-prompt baseline"
                   " · q27b", YESQ))
    # matched random pairs (controls) at the workspace band
    for seed in (1, 2):
        s.append(_spec(f"a12-swap-ws-r{seed}-q27b",
                       f"Swap no<->yes ws-band RAND pair seed {seed} · q27b",
                       FEELS, steer=_swap(WS, 1.0, rand_seed=seed)))
    # the swaps
    s.append(_spec("a12-swap-ws-q27b",
                   "Swap no<->yes ws-band L28-56 alpha=1 · q27b",
                   FEELS, steer=_swap(WS, 1.0)))
    s.append(_spec("a12-swap-ws-a2-q27b",
                   "Swap no<->yes ws-band L28-56 alpha=2 · q27b",
                   FEELS, steer=_swap(WS, 2.0)))
    s.append(_spec("a12-swap-deep-q27b",
                   "Swap no<->yes deep L52-62 alpha=1 · q27b",
                   FEELS, steer=_swap(DEEP, 1.0)))
    # the symmetry discriminator: same swap on the Yes-answer prompt
    # (rand control before the steered arm, u5c rule)
    s.append(_spec("a12-yes-swap-ws-r1-q27b",
                   "Swap RAND pair seed 1 on yes-prompt · q27b",
                   YESQ, steer=_swap(WS, 1.0, rand_seed=1)))
    s.append(_spec("a12-yes-swap-ws-q27b",
                   "Swap no<->yes ws-band on yes-prompt alpha=1 · q27b",
                   YESQ, steer=_swap(WS, 1.0)))
    return s


def run() -> None:
    ids = []
    for spec in specs():
        print(f"== {spec['id']}", flush=True)
        lab.run(spec)
        ids.append(spec["id"])
    # ribbons (full-instrument default), same process/model load
    import apparatus11
    apparatus11.capture(MODEL, record_ids=ids)


def report() -> None:
    lines = ["# apparatus-12 — Fig-4C concept swap, battery 1 (qwen-27b)",
             "", "Formula: MECHANICS 3d. Pair: no<->yes. "
             "calib = mean ||delta||/||h|| per hooked layer, averaged "
             "over ALL steered forward calls (generation + lens + "
             "vanilla replay), per the audit-02 report-the-calibration "
             "rule. Ranks are read at the ANSWER token (located by "
             "scanning the stored tokens for the first generated word), "
             "not at a fixed offset.",
             "", "| record | answer | ans tok | yes rank | no rank "
             "| calib (min-max) |", "|---|---|---|---|---|---|"]
    for spec in specs():
        p = lab.RESULTS / spec["id"] / "record.json"
        if not p.exists():
            lines.append(f"| `{spec['id']}` | MISSING | | | | |")
            continue
        rec = json.loads(p.read_text())
        gen = "".join(rec.get("generated", []) or []).strip()
        answer = gen.split("\n")[0][:40] or "(empty)"
        # locate the answer token in the lens tokenization: first token
        # in the generated tail whose stripped form starts the answer
        toks = rec["tokens"]
        first = (answer.split() or ["?"])[0].strip("*").rstrip(".,!")
        ans_idx = None
        tail_start = max(0, len(toks) - len(rec.get("generated", [])) - 2)
        for i in range(tail_start, len(toks)):
            if first and toks[i].strip().lower().startswith(
                    first[:4].lower()):
                ans_idx = i
                break
        # the lens readout at position p predicts token p+1, so the
        # answer token at ans_idx is read at position ans_idx - 1
        mouth, ans_tok = {}, "?"
        for t in rec["trajectories"]:
            if t["word"] in ("yes", "no") and ans_idx is not None \
                    and t["position"] == ans_idx - 1:
                mouth[t["word"]] = t["ranks"][-1]
                ans_tok = toks[ans_idx]
        if ans_idx is not None and not mouth:
            ans_tok = f"{toks[ans_idx]} (outside readout window)"
        cal = ""
        if rec.get("steer_calib"):
            vals = [v for d in rec["steer_calib"] for v in d.values()]
            cal = f"{min(vals):.4f}-{max(vals):.4f}"
        lines.append(
            f"| `{spec['id']}` | {answer} | {ans_tok} "
            f"| {mouth.get('yes', '-')} | {mouth.get('no', '-')} "
            f"| {cal} |")
    OUTDIR.mkdir(exist_ok=True)
    p = OUTDIR / "report.md"
    p.write_text("\n".join(lines) + "\n")
    print(f"wrote {p}", flush=True)


if __name__ == "__main__":
    {"run": run, "report": report}[sys.argv[1]]()
