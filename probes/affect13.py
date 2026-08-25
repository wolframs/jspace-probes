"""affect-13 — dynamics of the exit gate. Prereg:
results/affect13-prereg.md (frozen before run).

Full-roster instrumented re-run of the affect-08 pulse harness: every
free step records RAW logits (output_logits — the top-k-filtered
scores of _sample are -inf at filtered tokens, the affect-05/07 trap)
for the exit token, the loop token, and top-1/top-2. CRN seeds mean
the trajectories re-generate affect-08's outcomes bit-identically.

Usage:
  .venv/bin/python probes/affect13.py run
  .venv/bin/python probes/affect13.py analyze
"""

import json
import sys
from collections import Counter

import torch

from lab import RESULTS, Steering, get_model
from affect2 import _load_vectors
from affect3 import AffectSteer, E_LAYERS
from affect7 import (CFG, PRE, PULSE, POST, WINDOW, TEMP, N_STEER,
                     _exit_id, _prompt_ids)
from affect11 import _pullback
from fanout import TYPO
from loops import loop_gram

MODEL = "qwen-27b"
AE = 0.08
SEEDS = list(range(16))
OUT = RESULTS / "affect13-q27b"
ANGER = ["angry", "hostile", "exasperated"]
PRIDE = ["proud", "enthusiastic"]


class _NoCtx:
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _sample_raw(lm, ids, n, ctx=None, seed=None):
    """Sampled continuation returning (sequences, per-step RAW logits)."""
    if seed is not None:
        torch.manual_seed(seed)
    mgr = ctx if ctx is not None else _NoCtx()
    with mgr, torch.no_grad():
        out = lm.model._hf_model.generate(
            ids, max_new_tokens=n, do_sample=True, temperature=TEMP,
            output_logits=True, return_dict_in_generate=True)
    return out.sequences, list(out.logits)


def _trace(logits, exit_id, loop_id):
    """Per-step [exit_logit, loop_logit, top1_logit, top2_logit,
    top1_id, top2_id], rounded."""
    rows = []
    for lg in logits:
        v = lg[0].float()
        t2 = torch.topk(v, 2)
        rows.append([round(float(v[exit_id]), 3),
                     round(float(v[loop_id]), 3),
                     round(float(t2.values[0]), 3),
                     round(float(t2.values[1]), 3),
                     int(t2.indices[0]), int(t2.indices[1])])
    return rows


def run() -> None:
    cfg = CFG[MODEL]
    OUT.mkdir(parents=True, exist_ok=True)
    lm = get_model(MODEL)
    ids = _prompt_ids(lm, MODEL)
    exit_id = _exit_id(lm, MODEL)

    Vemo, emos = _load_vectors(MODEL)
    Vtok = _pullback(lm, [" table"], extra_ids=[exit_id])

    with Steering(lm, TYPO, cfg["mid"], "amplify",
                  cfg["alpha_typo"]), torch.no_grad():
        forced = lm.model._hf_model.generate(
            ids, max_new_tokens=N_STEER, do_sample=False)
    ftext = lm.tok.decode(forced[0, ids.shape[1]:], skip_special_tokens=True)
    g1, n1 = loop_gram(ftext)
    lw = (g1.split()[0] if g1 else "luckily").lower()
    loop_id = Counter(forced[0, -20:].tolist()).most_common(1)[0][0]
    print(f"forced loop4={g1!r}x{n1} loopword={lw!r} "
          f"loop_id={loop_id}={lm.tok.decode([loop_id])!r}", flush=True)

    conds = [("none", "none", None)]
    for e in emos:
        i = emos.index(e)
        conds.append((e, "emotion",
                      (lambda i=i: AffectSteer(lm, Vemo, i, E_LAYERS,
                                               "amplify", AE))))
    for r in (1, 2):
        conds.append((f"rand{r}", "random",
                      (lambda r=r: AffectSteer(lm, Vemo, 0, E_LAYERS,
                                               "amplify", AE,
                                               rand_seed=r))))
    conds.append(("table", "token",
                  lambda: AffectSteer(lm, Vtok, 0, E_LAYERS,
                                      "amplify", AE)))
    conds.append(("exitdir", "exitdir",
                  lambda: AffectSteer(lm, Vtok, 1, E_LAYERS,
                                      "amplify", AE)))
    print(f"{len(conds)} conditions x {len(SEEDS)} seeds @ ae={AE}",
          flush=True)

    ck = OUT / "affect13.json"
    if ck.exists():
        res = json.loads(ck.read_text())
        assert res["loopword"] == lw
        done = {r["seed"] for r in res["runs"]}
        print(f"resuming: seeds {sorted(done)} complete", flush=True)
    else:
        res = {"model": MODEL, "alpha_e": AE, "e_layers": E_LAYERS,
               "seeds": SEEDS, "forced_loop4": [g1, n1], "loopword": lw,
               "loop_id": loop_id, "exit_id": exit_id,
               "pre": PRE, "pulse": PULSE, "post": POST,
               "window": WINDOW,
               "conditions": [(c[0], c[1]) for c in conds], "runs": []}
        done = set()

    for seed in SEEDS:
        if seed in done:
            continue
        seq1, lg1 = _sample_raw(lm, forced, PRE, seed=seed)
        if seq1.shape[1] < forced.shape[1] + PRE:
            print(f"  seed {seed}: escaped before pulse — skipped",
                  flush=True)
            continue
        tr1 = _trace(lg1, exit_id, loop_id)
        for name, kind, factory in conds:
            ctx = factory() if factory is not None else None
            seq2, lg2 = _sample_raw(lm, seq1, PULSE, ctx=ctx,
                                    seed=seed + 10_000)
            tr2 = _trace(lg2, exit_id, loop_id)
            if seq2.shape[1] < seq1.shape[1] + PULSE:
                seq3, tr3 = seq2, []
            else:
                seq3, lg3 = _sample_raw(lm, seq2, POST,
                                        seed=seed + 20_000)
                tr3 = _trace(lg3, exit_id, loop_id)
            free = seq3[0, forced.shape[1]:]
            n_free = len(free)
            exited = n_free < PRE + PULSE + POST
            exit_step = n_free if exited else None
            res["runs"].append({
                "seed": seed, "cond": name, "kind": kind,
                "n_steps": n_free,
                "exited": exited, "exit_step": exit_step,
                "turnend_in_window": bool(
                    exit_step is not None
                    and PRE <= exit_step < PRE + WINDOW),
                "trace": tr1 + tr2 + tr3})
            r = res["runs"][-1]
            print(f"  s{seed} {name:<13} exit={exit_step} "
                  f"turnend@W={r['turnend_in_window']}", flush=True)
        (OUT / "affect13.json").write_text(json.dumps(res))
    print("RUN DONE", flush=True)


def analyze() -> None:
    import itertools
    import random as _random
    res = json.loads((OUT / "affect13.json").read_text())
    runs = res["runs"]
    kind = dict(res["conditions"])
    loop_id, exit_id = res["loop_id"], res["exit_id"]
    pre, pulse = res["pre"], res["pulse"]

    def a8pot():
        out = {}
        for path in ("affect08-q27b-ae08", "affect08-q27b-ae1"):
            d = json.loads(
                (RESULTS / path / "affect08.json").read_text())
            for c in {r["cond"] for r in d["runs"]}:
                rs = [r for r in d["runs"] if r["cond"] == c]
                out.setdefault(c, []).append(
                    sum(r["turnend_in_window"] for r in rs) / len(rs))
        return {k: sum(v) / len(v) for k, v in out.items()}
    pot = a8pot()

    none_tr = {r["seed"]: r["trace"] for r in runs if r["cond"] == "none"}

    def dexit(r):
        """pulse exit lift vs same-seed none, mean over shared pulse
        steps."""
        nt = none_tr.get(r["seed"])
        if nt is None:
            return None
        ds = []
        for t in range(pre, min(pre + pulse, len(r["trace"]),
                                len(nt))):
            ds.append(r["trace"][t][0] - nt[t][0])
        return sum(ds) / len(ds) if ds else None

    per_dir = {}
    for name in {r["cond"] for r in runs} - {"none"}:
        vals = [dexit(r) for r in runs if r["cond"] == name]
        vals = [v for v in vals if v is not None]
        per_dir[name] = sum(vals) / len(vals)

    lines = ["# affect-13 — dynamics of the exit gate (qwen-27b, "
             f"ae={res['alpha_e']})", "",
             "| cond | kind | dExit(pulse) | potency(a08) |",
             "|---|---|---|---|"]
    for n in sorted(per_dir, key=lambda n: -per_dir[n]):
        p = f"{pot[n]:.3f}" if n in pot else "—"
        lines.append(f"| {n} | {kind[n]} | {per_dir[n]:+.2f} | {p} |")

    # P-a
    def spearman(x, y):
        def rank(v):
            s = sorted(range(len(v)), key=lambda i: v[i])
            r = [0.0] * len(v)
            for i, j in enumerate(s):
                r[j] = i
            return r
        rx, ry = rank(x), rank(y)
        n = len(x)
        mx, my = sum(rx) / n, sum(ry) / n
        num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
        den = (sum((a - mx) ** 2 for a in rx)
               * sum((b - my) ** 2 for b in ry)) ** 0.5
        return num / den if den else 0.0
    emo = [n for n in per_dir if kind[n] == "emotion"]
    xs = [per_dir[n] for n in emo]
    ys = [pot[n] for n in emo]
    rho = spearman(xs, ys)
    rng = _random.Random(2718)
    ge, N = 0, 20000
    for _ in range(N):
        sh = ys[:]
        rng.shuffle(sh)
        if abs(spearman(xs, sh)) >= abs(rho) - 1e-12:
            ge += 1
    lines += ["", "## P-a potency vs pulse exit lift (24 emotions)",
              f"- Spearman {rho:+.3f}, permutation p={ge / N:.4f}"
              f"{' (sig .05)' if ge / N < .05 else ''}"
              f"  (prereg bar: rho >= .5 AND p < .05)"]

    # P-b sign report
    lines += ["", "## P-b two floors (descriptive, per prereg)"]
    for fam, names in (("anger", ANGER), ("pride", PRIDE)):
        for n in names:
            lines.append(f"- {fam}: {n:<13} dExit {per_dir[n]:+.2f}")

    # P-c / P-d event-order classifier
    def classify(r):
        tr = r["trace"]
        for t in range(pre, min(pre + pulse + res["window"], len(tr))):
            exit_top2 = exit_id in (tr[t][4], tr[t][5])
            deloop = tr[t][4] != loop_id
            if exit_top2 and not deloop:
                return "door_first"
            if deloop and not exit_top2:
                return "deloop_first"
            if exit_top2 and deloop:
                return "same_step"
        return "neither"
    lines += ["", "## P-c/P-d event order (first crossing in "
              "pulse..pulse+W)", "",
              "| cond | door_first | deloop_first | same_step | neither |",
              "|---|---|---|---|---|"]
    potent = [n for n in emo if pot.get(n, 0) >= 0.75]
    for name in sorted(potent) + ["table", "exitdir", "rand1", "rand2"]:
        cs = Counter(classify(r) for r in runs if r["cond"] == name)
        lines.append(f"| {name} | {cs['door_first']} | "
                     f"{cs['deloop_first']} | {cs['same_step']} | "
                     f"{cs['neither']} |")
    pooled = Counter(classify(r) for r in runs
                     if r["cond"] in potent)
    lines += ["", f"- pooled potent-emotion runs: {dict(pooled)}"]

    (OUT / "report.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "run"
    if what == "run":
        run()
    elif what == "analyze":
        analyze()
    print("DONE", flush=True)
