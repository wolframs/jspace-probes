"""affect-08 — dose-resolved replication at the discriminating alpha_e,
direction-level inference, turn-end primary endpoint. Plus oneoffs-04
(matched-text release control for u18) in the same load.

Successor to affect-07 per the 2026-08-09 sweep corrections:
  - DIRECTION is the inferential unit (seeds are repeats, not samples);
  - primary endpoint is ACTUAL TURN-END within the window (composite
    escape admits loop-replacement);
  - full 24-emotion roster labelled on BOTH valence and arousal, so the
    run adjudicates VALENCE vs AROUSAL vs settled-pole vs flat;
  - 16 Gaussian directions, not two;
  - alpha_e in {0.08, 0.10}: between affect-07's near-extinguished 0.06
    and its saturated 0.12.

Machinery is affect-07's three-phase pulse harness verbatim (shared
phase 1 per seed, common random numbers in phases 2/3): see affect7.py
for the pulse convention. Prereg: results/affect08-prereg.md (frozen
before the run).

oneoffs-04 (`release`): hand an UNSTEERED model the u18-hyst steered
prefixes as bare text — dose (a0420/a0480/a0680) x truncation length
(15/30/50 tokens) x 8 sampled seeds, plus a shuffled-repeat arm (same
tokens, repeat region order destroyed) and the a0000 protocol control.
Note the u18 release pass already recomputes from ids (loops.py), so
latent cross-call state is excluded by construction; what this measures
is the transcript-attractor's basin: persistence hazard as a function
of dose and repeat count, and whether it needs the exact n-gram.

Usage:
  .venv/bin/python probes/affect8.py run qwen-27b 0.10
  .venv/bin/python probes/affect8.py run qwen-27b 0.08
  .venv/bin/python probes/affect8.py release
  .venv/bin/python probes/affect8.py analyze qwen-27b 0.10
"""

import json
import random
import sys

import torch

from lab import CONFIGS, RESULTS, Steering, _strip_bos, get_model
import lab
from affect import EMOTIONS
from affect2 import _load_vectors
from affect3 import AffectSteer
from affect7 import (CFG, PRE, PULSE, POST, WINDOW, TEMP, N_STEER,
                     _exit_id, _prompt_ids, _sample, _events)
from concepts import outdir as a6dir
from fanout import TYPO
from loops import loop_gram

SEEDS = list(range(16))
N_GAUSS = 16

# Frozen arousal labels (core-affect circumplex, binary; prereg §labels).
AROUSAL = {
    "happy": +1, "enthusiastic": +1, "proud": +1, "hopeful": +1,
    "curious": +1, "angry": +1, "afraid": +1, "anxious": +1,
    "distressed": +1, "desperate": +1, "hostile": +1, "exasperated": +1,
    "nervous": +1, "vigilant": +1,
    "calm": -1, "content": -1, "blissful": -1, "grateful": -1,
    "loving": -1, "sad": -1, "gloomy": -1, "brooding": -1, "guilty": -1,
    "reflective": -1,
}


def outdir(model: str, alpha_e: float):
    tag = CFG[model]["tag"] + f"-ae{alpha_e:g}".replace("0.", "")
    d = RESULTS / f"affect08-{tag}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _conditions(lm, model: str, alpha_e: float):
    """[(name, kind, factory-or-None, valence, arousal)]"""
    lay = CFG[model]["e_layers"]
    V, emos = _load_vectors(model)
    cv = torch.load(a6dir(model) / "cvectors.pt")
    C, slugs = cv["anthropic"], cv["slugs"]
    conds = [("none", "none", None, 0, 0)]
    for e in EMOTIONS:                       # all 24
        i = emos.index(e)
        conds.append((e, "emotion",
                      (lambda i=i: AffectSteer(lm, V, i, lay,
                                               "amplify", alpha_e)),
                      EMOTIONS[e], AROUSAL[e]))
    for j, sl in enumerate(slugs):
        conds.append((sl, "concept",
                      (lambda j=j: AffectSteer(lm, C, j, lay,
                                               "amplify", alpha_e)), 0, 0))
    for r in range(1, N_GAUSS + 1):
        conds.append((f"rand{r}", "random",
                      (lambda r=r: AffectSteer(lm, V, 0, lay,
                                               "amplify", alpha_e,
                                               rand_seed=r)), 0, 0))
    return conds


def run(model: str, alpha_e: float) -> None:
    cfg = CFG[model]
    OUT = outdir(model, alpha_e)
    lm = get_model(model)
    ids = _prompt_ids(lm, model)
    im_end = _exit_id(lm, model)

    with Steering(lm, TYPO, cfg["mid"], "amplify",
                  cfg["alpha_typo"]), torch.no_grad():
        forced = lm.model._hf_model.generate(
            ids, max_new_tokens=N_STEER, do_sample=False)
    ftext = lm.tok.decode(forced[0, ids.shape[1]:], skip_special_tokens=True)
    g1, n1 = loop_gram(ftext)
    lw = (g1.split()[0] if g1 else "luckily").lower()
    print(f"forced loop4={g1!r}x{n1} loopword={lw!r}", flush=True)

    conds = _conditions(lm, model, alpha_e)
    print(f"{len(conds)} conditions x {len(SEEDS)} seeds "
          f"@ ae={alpha_e}", flush=True)
    # Resume: every phase is seeded and the forced phase is greedy, so a
    # restarted process regenerates the same sequences. Only complete
    # seeds are checkpointed, so skipping them is exact.
    ck = OUT / "affect08.json"
    if ck.exists():
        res = json.loads(ck.read_text())
        assert res["loopword"] == lw, (res["loopword"], lw)
        done = {r["seed"] for r in res["runs"]}
        print(f"resuming: seeds {sorted(done)} already complete",
              flush=True)
    else:
        res = {"model": model, "alpha_typo": cfg["alpha_typo"],
               "mid": cfg["mid"], "e_layers": cfg["e_layers"],
               "alpha_e": alpha_e, "temp": TEMP,
               "pre": PRE, "pulse": PULSE, "post": POST, "window": WINDOW,
               "seeds": SEEDS, "forced_loop4": [g1, n1], "loopword": lw,
               "conditions": [(c[0], c[1], c[3], c[4]) for c in conds],
               "runs": []}
        done = set()

    for seed in SEEDS:
        if seed in done:
            continue
        seq1, _sc1 = _sample(lm, forced, PRE, seed=seed)
        if seq1.shape[1] < forced.shape[1] + PRE:
            print(f"  seed {seed}: escaped before pulse — skipped",
                  flush=True)
            continue
        for name, kind, factory, val, aro in conds:
            ctx = factory() if factory is not None else None
            seq2, _ = _sample(lm, seq1, PULSE, ctx=ctx, seed=seed + 10_000)
            if seq2.shape[1] < seq1.shape[1] + PULSE:
                seq3 = seq2
            else:
                seq3, _ = _sample(lm, seq2, POST, seed=seed + 20_000)
            free = seq3[0, forced.shape[1]:]
            toks = [lm.tok.decode([int(t)]) for t in free]
            deloop = _events(toks, lw, PRE)
            exited = len(free) < PRE + PULSE + POST
            exit_step = len(free) if exited else None
            res["runs"].append({
                "seed": seed, "cond": name, "kind": kind,
                "valence": val, "arousal": aro, "n_steps": len(free),
                "deloop_step": deloop,
                "exited": exited, "exit_step": exit_step,
                "turnend_in_window": bool(
                    exit_step is not None
                    and PRE <= exit_step < PRE + WINDOW),
                "loop_frac_post": round(
                    sum(lw in t.lower() for t in toks[PRE:])
                    / max(1, len(toks) - PRE), 3),
                "text_tail": "".join(toks)[-80:]})
            r = res["runs"][-1]
            print(f"  s{seed} {name:<13} exit={exit_step} "
                  f"turnend@W={r['turnend_in_window']} "
                  f"lf={r['loop_frac_post']}", flush=True)
        (OUT / "affect08.json").write_text(json.dumps(res, indent=1))
    print("RUN DONE", flush=True)


# ------------------------------------------------- oneoffs-04: release
REL_DOSES = ["a0000", "a0420", "a0480", "a0680"]
REL_LENS = [15, 30, 50]
REL_SEEDS = list(range(8))
REL_FREE = 100


def release(model: str = "qwen-27b") -> None:
    lm = get_model(model)
    tok = lm.tok
    ids = _prompt_ids(lm, model)
    out = {"model": model, "free": REL_FREE, "runs": []}
    for dose in REL_DOSES:
        rec = json.loads((RESULTS / f"u18-hyst-{dose}-q27b" /
                          "record.json").read_text())
        md = rec["extra_md"]
        steered = md["steered_text"]
        lw = (md["loop4_steered"][0].split()[0]
              if md["loop4_steered"][0] else "luckily").lower()
        st_ids = tok(steered, add_special_tokens=False,
                     return_tensors="pt").input_ids
        lens = REL_LENS if dose != "a0000" else [50]
        arms = [(f"len{n}", st_ids[:, :n]) for n in lens]
        if dose != "a0000":
            # shuffled-repeat arm: keep the first 10 tokens (the intact
            # sentence head), shuffle the remaining 40 in place.
            sh = st_ids[0].tolist()
            head, tail = sh[:10], sh[10:50]
            random.Random(31459).shuffle(tail)
            arms.append(("shuf50",
                         torch.tensor([head + tail], dtype=st_ids.dtype)))
        for arm, part in arms:
            full = torch.cat([ids, part.to(ids.device)], dim=1)
            for seed in REL_SEEDS:
                seq, _ = _sample(lm, full, REL_FREE, seed=seed)
                free = seq[0, full.shape[1]:]
                toks = [tok.decode([int(t)]) for t in free]
                deloop = _events(toks, lw, 0)
                exited = len(free) < REL_FREE
                out["runs"].append({
                    "dose": dose, "arm": arm, "seed": seed,
                    "loopword": lw, "n_steps": len(free),
                    "deloop_step": deloop, "exited": exited,
                    "loop_frac": round(
                        sum(lw in t.lower() for t in toks)
                        / max(1, len(toks)), 3),
                    "tail": "".join(toks)[-70:]})
                r = out["runs"][-1]
                print(f"  {dose} {arm:<6} s{seed} lf={r['loop_frac']} "
                      f"deloop={deloop}", flush=True)
    d = RESULTS / "oneoffs04-release-q27b"
    d.mkdir(parents=True, exist_ok=True)
    (d / "release.json").write_text(json.dumps(out, indent=1))
    print("RELEASE DONE", flush=True)


# ------------------------------------------------------------ analysis
def analyze(model: str, alpha_e: float) -> None:
    OUT = outdir(model, alpha_e)
    res = json.loads((OUT / "affect08.json").read_text())
    runs = res["runs"]
    conds = res["conditions"]
    import itertools
    from affect7 import _spearman

    def per_dir(key):
        d = {}
        for name, kind, val, aro in conds:
            rs = [r for r in runs if r["cond"] == name]
            if rs:
                d[name] = sum(float(r[key]) for r in rs) / len(rs)
        return d

    te = per_dir("turnend_in_window")
    lf = per_dir("loop_frac_post")
    kind = {c[0]: c[1] for c in conds}
    val = {c[0]: c[2] for c in conds}
    aro = {c[0]: c[3] for c in conds}
    emo = [n for n in te if kind[n] == "emotion"]
    con = [n for n in te if kind[n] == "concept"]
    rnd = [n for n in te if kind[n] == "random"]

    def mean(xs):
        return sum(xs) / len(xs) if xs else 0.0

    lines = [f"# affect-08 ae={alpha_e} ({model}) — direction-level",
             "",
             f"| cond | kind | val | aro | turnend@W | loopfrac |",
             "|---|---|---|---|---|---|"]
    for n in sorted(te, key=lambda n: -te[n]):
        lines.append(f"| {n} | {kind[n]} | {val[n]:+d} | {aro[n]:+d} "
                     f"| {te[n]:.3f} | {lf[n]:.3f} |")
    lines += ["", "## PRIMARY turn-end@window, direction-level", "",
              f"- none: {te.get('none', 0):.3f}",
              f"- emotions n={len(emo)} mean {mean([te[n] for n in emo]):.3f}",
              f"- concepts n={len(con)} mean {mean([te[n] for n in con]):.3f}",
              f"- randoms n={len(rnd)} mean {mean([te[n] for n in rnd]):.3f}"]

    # 2x2 on the emotion roster: valence / arousal / interaction,
    # exact permutation over balanced relabelings where feasible,
    # else 20k Monte Carlo.
    scores = [te[n] for n in emo]

    def contrast(labels):
        a = [s for s, l in zip(scores, labels) if l > 0]
        b = [s for s, l in zip(scores, labels) if l < 0]
        return mean(a) - mean(b)

    rng = random.Random(2718)
    for eff, labels in [("valence", [val[n] for n in emo]),
                        ("arousal", [aro[n] for n in emo]),
                        ("interaction",
                         [val[n] * aro[n] for n in emo])]:
        lab_nonzero = [l for l in labels if l != 0]
        sc = [s for s, l in zip(scores, labels) if l != 0]

        def c(ls, sc=sc):
            a = [s for s, l in zip(sc, ls) if l > 0]
            b = [s for s, l in zip(sc, ls) if l < 0]
            return mean(a) - mean(b)
        obs = c(lab_nonzero)
        ge, N = 0, 20000
        for _ in range(N):
            sh = lab_nonzero[:]
            rng.shuffle(sh)
            if abs(c(sh)) >= abs(obs) - 1e-12:
                ge += 1
        lines.append(f"- {eff}: gap {obs:+.3f}, permutation "
                     f"p={ge / N:.4f}"
                     f"{' (sig .05)' if ge / N < .05 else ''}")

    # settled pole (prereg): pos-valence x low-arousal quadrant vs rest
    pole = [n for n in emo if val[n] > 0 and aro[n] < 0]
    rest = [n for n in emo if n not in pole]
    obs = mean([te[n] for n in pole]) - mean([te[n] for n in rest])
    ge, N = 0, 20000
    for _ in range(N):
        sh = emo[:]
        rng.shuffle(sh)
        if abs(mean([te[n] for n in sh[:len(pole)]])
               - mean([te[n] for n in sh[len(pole):]])) >= abs(obs) - 1e-12:
            ge += 1
    lines.append(f"- settled-pole (pos/low-arousal {pole} vs rest): "
                 f"gap {obs:+.3f}, p={ge / N:.4f}"
                 f"{' (sig .05)' if ge / N < .05 else ''}")

    # emotion vs concept, emotion vs random, concept vs random
    for la, lb, A, B in [("emotion", "concept", emo, con),
                         ("emotion", "random", emo, rnd),
                         ("concept", "random", con, rnd)]:
        allv = [te[n] for n in A] + [te[n] for n in B]
        obs = mean([te[n] for n in A]) - mean([te[n] for n in B])
        ge, N = 0, 20000
        for _ in range(N):
            rng.shuffle(allv)
            if abs(mean(allv[:len(A)]) - mean(allv[len(A):])) \
                    >= abs(obs) - 1e-12:
                ge += 1
        lines.append(f"- {la} vs {lb}: gap {obs:+.3f}, p={ge / N:.4f}"
                     f"{' (sig .05)' if ge / N < .05 else ''}")

    (OUT / "report.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "run"
    mdl = sys.argv[2] if len(sys.argv) > 2 else "qwen-27b"
    ae = float(sys.argv[3]) if len(sys.argv) > 3 else 0.10
    if what == "run":
        run(mdl, ae)
    elif what == "release":
        release(mdl)
    elif what == "analyze":
        analyze(mdl, ae)
    print("DONE", flush=True)
