"""affect-14 — margin-primary replication (fresh seeds) + coupling
locus (single-layer sufficiency / leave-one-layer-out necessity).
Prereg: results/affect14-prereg.md (frozen before run). Reuses the
affect-13 raw-logit trace machinery verbatim.

Usage:
  .venv/bin/python probes/affect14.py run1     # Part 1, seeds 16-27
  .venv/bin/python probes/affect14.py run2     # Part 2, seeds 16-23
  .venv/bin/python probes/affect14.py analyze
"""

import json
import sys
from collections import Counter

import torch

from lab import RESULTS, Steering, get_model
from affect2 import _load_vectors
from affect3 import AffectSteer, E_LAYERS
from affect7 import (CFG, PRE, PULSE, POST, WINDOW, N_STEER,
                     _exit_id, _prompt_ids)
from affect11 import _pullback
from affect13 import _sample_raw, _trace
from fanout import TYPO
from loops import loop_gram

MODEL = "qwen-27b"
AE = 0.08
SEEDS1 = list(range(16, 28))
SEEDS2 = list(range(16, 24))
OUT = RESULTS / "affect14-q27b"
FLOOR = ["angry", "proud", "enthusiastic", "hostile", "exasperated"]
CASE = ["calm", "proud", "table"]


def _forced(lm, ids):
    cfg = CFG[MODEL]
    with Steering(lm, TYPO, cfg["mid"], "amplify",
                  cfg["alpha_typo"]), torch.no_grad():
        forced = lm.model._hf_model.generate(
            ids, max_new_tokens=N_STEER, do_sample=False)
    ftext = lm.tok.decode(forced[0, ids.shape[1]:],
                          skip_special_tokens=True)
    g1, n1 = loop_gram(ftext)
    lw = (g1.split()[0] if g1 else "luckily").lower()
    loop_id = Counter(forced[0, -20:].tolist()).most_common(1)[0][0]
    print(f"forced loop4={g1!r}x{n1} loopword={lw!r}", flush=True)
    return forced, g1, n1, lw, loop_id


def _grid(lm, tag, conds, seeds, forced, meta):
    ck = OUT / f"affect14-{tag}.json"
    if ck.exists():
        res = json.loads(ck.read_text())
        assert res["loopword"] == meta["loopword"]
        done = {r["seed"] for r in res["runs"]}
        print(f"{tag}: resuming, seeds {sorted(done)} complete",
              flush=True)
    else:
        res = dict(meta)
        res.update({"conditions": [(c[0], c[1]) for c in conds],
                    "seeds": seeds, "runs": []})
        done = set()
    exit_id, loop_id = meta["exit_id"], meta["loop_id"]
    for seed in seeds:
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
                "n_steps": n_free, "exited": exited,
                "exit_step": exit_step,
                "turnend_in_window": bool(
                    exit_step is not None
                    and PRE <= exit_step < PRE + WINDOW),
                "trace": tr1 + tr2 + tr3})
            print(f"  [{tag}] s{seed} {name:<16} exit={exit_step}",
                  flush=True)
        ck.write_text(json.dumps(res))
    print(f"{tag} DONE", flush=True)


def _setup():
    OUT.mkdir(parents=True, exist_ok=True)
    lm = get_model(MODEL)
    ids = _prompt_ids(lm, MODEL)
    exit_id = _exit_id(lm, MODEL)
    Vemo, emos = _load_vectors(MODEL)
    Vtok = _pullback(lm, [" table"], extra_ids=[exit_id])
    forced, g1, n1, lw, loop_id = _forced(lm, ids)
    meta = {"model": MODEL, "alpha_e": AE, "e_layers": E_LAYERS,
            "forced_loop4": [g1, n1], "loopword": lw,
            "loop_id": loop_id, "exit_id": exit_id,
            "pre": PRE, "pulse": PULSE, "post": POST, "window": WINDOW}
    return lm, Vemo, emos, Vtok, forced, meta


def _dir_ctx(lm, Vemo, emos, Vtok, name, layers):
    if name == "table":
        return lambda: AffectSteer(lm, Vtok, 0, layers, "amplify", AE)
    if name == "exitdir":
        return lambda: AffectSteer(lm, Vtok, 1, layers, "amplify", AE)
    i = emos.index(name)
    return lambda i=i: AffectSteer(lm, Vemo, i, layers, "amplify", AE)


def run1() -> None:
    lm, Vemo, emos, Vtok, forced, meta = _setup()
    conds = [("none", "none", None)]
    for e in emos:
        conds.append((e, "emotion",
                      _dir_ctx(lm, Vemo, emos, Vtok, e, E_LAYERS)))
    for r in (1, 2, 3, 4):
        conds.append((f"rand{r}", "random",
                      (lambda r=r: AffectSteer(lm, Vemo, 0, E_LAYERS,
                                               "amplify", AE,
                                               rand_seed=r))))
    conds.append(("table", "token",
                  _dir_ctx(lm, Vemo, emos, Vtok, "table", E_LAYERS)))
    conds.append(("exitdir", "exitdir",
                  _dir_ctx(lm, Vemo, emos, Vtok, "exitdir", E_LAYERS)))
    print(f"part1: {len(conds)} conds x {len(SEEDS1)} seeds", flush=True)
    _grid(lm, "part1", conds, SEEDS1, forced, meta)


def run2() -> None:
    lm, Vemo, emos, Vtok, forced, meta = _setup()
    conds = [("none", "none", None)]
    for d in CASE:
        conds.append((f"{d}_full", "full",
                      _dir_ctx(lm, Vemo, emos, Vtok, d, E_LAYERS)))
        for l in E_LAYERS:
            conds.append((f"{d}_only{l}", "single",
                          _dir_ctx(lm, Vemo, emos, Vtok, d, [l])))
            rest = [x for x in E_LAYERS if x != l]
            conds.append((f"{d}_no{l}", "lolo",
                          _dir_ctx(lm, Vemo, emos, Vtok, d, rest)))
    print(f"part2: {len(conds)} conds x {len(SEEDS2)} seeds", flush=True)
    _grid(lm, "part2", conds, SEEDS2, forced, meta)


# ------------------------------------------------------------ analysis
def _spearman(x, y):
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


def _deltas(res):
    pre, pulse = res["pre"], res["pulse"]
    none = {r["seed"]: r["trace"] for r in res["runs"]
            if r["cond"] == "none"}

    def d(r, idx):
        nt = none.get(r["seed"])
        if nt is None:
            return None
        ds = [r["trace"][t][idx] - nt[t][idx]
              for t in range(pre, min(pre + pulse, len(r["trace"]),
                                      len(nt)))]
        return sum(ds) / len(ds) if ds else None

    out = {}
    for name in {r["cond"] for r in res["runs"]} - {"none"}:
        de, dl = [], []
        for r in res["runs"]:
            if r["cond"] != name:
                continue
            a, b = d(r, 0), d(r, 1)
            if a is not None:
                de.append(a)
                dl.append(b)
        out[name] = (sum(de) / len(de), sum(dl) / len(dl))
    return out


def analyze() -> None:
    import random as _random
    rng = _random.Random(2718)
    lines = ["# affect-14 — margin-primary + coupling locus "
             f"(qwen-27b, ae={AE})", ""]

    # ---- Part 1
    res1 = json.loads((OUT / "affect14-part1.json").read_text())
    kind = dict(res1["conditions"])
    dd = _deltas(res1)
    pot = {}
    for path in ("affect08-q27b-ae08", "affect08-q27b-ae1"):
        d8 = json.loads((RESULTS / path / "affect08.json").read_text())
        for c in {r["cond"] for r in d8["runs"]}:
            rs = [r for r in d8["runs"] if r["cond"] == c]
            pot.setdefault(c, []).append(
                sum(r["turnend_in_window"] for r in rs) / len(rs))
    pot = {k: sum(v) / len(v) for k, v in pot.items()}

    lines += ["## Part 1 (fresh seeds 16-27)", "",
              "| cond | kind | dExit | dLoop | dMargin | potency |",
              "|---|---|---|---|---|---|"]
    margin = {n: de - dl for n, (de, dl) in dd.items()}
    for n in sorted(margin, key=lambda n: -margin[n]):
        de, dl = dd[n]
        p = f"{pot[n]:.3f}" if n in pot else "—"
        lines.append(f"| {n} | {kind[n]} | {de:+.2f} | {dl:+.2f} | "
                     f"{margin[n]:+.2f} | {p} |")

    emo = [n for n in margin if kind[n] == "emotion"]
    for label, vals in (("P-a dMargin (PRIMARY)",
                         [margin[n] for n in emo]),
                        ("secondary dExit",
                         [dd[n][0] for n in emo])):
        ys = [pot[n] for n in emo]
        rho = _spearman(vals, ys)
        ge, N = 0, 20000
        for _ in range(N):
            sh = ys[:]
            rng.shuffle(sh)
            if abs(_spearman(vals, sh)) >= abs(rho) - 1e-12:
                ge += 1
        lines.append(f"- {label}: Spearman {rho:+.3f}, "
                     f"p={ge / N:.4f}"
                     f"{' (sig .05)' if ge / N < .05 else ''}")

    rands = [abs(margin[f"rand{r}"]) for r in (1, 2, 3, 4)]
    fl = sum(abs(margin[n]) for n in FLOOR) / len(FLOOR)
    lines += [f"- P-b floor mean |dMargin| {fl:.2f} vs randoms max "
              f"|dMargin| {max(rands):.2f} -> "
              f"{'PASS (inside)' if fl <= max(rands) else 'FAIL (outside)'}",
              ""]

    # ---- Part 2
    res2 = json.loads((OUT / "affect14-part2.json").read_text())
    dd2 = _deltas(res2)
    lines += ["## Part 2 — coupling locus (seeds 16-23)", ""]
    for d in CASE:
        full_de, full_dl = dd2[f"{d}_full"]
        full_m = full_de - full_dl
        lines += [f"### {d} (full-stack dLoop {full_dl:+.2f}, "
                  f"dMargin {full_m:+.2f})", "",
                  "| layer | only-dLoop | %of-full | only-dMargin "
                  "| no-dLoop | %lost |",
                  "|---|---|---|---|---|---|"]
        best_frac, worst_loss = 0.0, 0.0
        for l in E_LAYERS:
            oe, ol = dd2[f"{d}_only{l}"]
            n_ = dd2[f"{d}_no{l}"][1]
            frac = ol / full_dl if full_dl else 0.0
            loss = 1 - (n_ / full_dl) if full_dl else 0.0
            best_frac = max(best_frac, frac)
            worst_loss = max(worst_loss, loss)
            lines.append(f"| L{l} | {ol:+.2f} | {frac:+.0%} | "
                         f"{oe - ol:+.2f} | {n_:+.2f} | {loss:+.0%} |")
        cls = ("CONCENTRATED" if best_frac >= .5 else
               "DISTRIBUTED" if best_frac <= .25 else "GRADED")
        lines += [f"- P-c class: {cls} (best single {best_frac:+.0%}); "
                  f"P-d worst LOLO loss {worst_loss:+.0%}", ""]
    ca = [dd2[f"calm_only{l}"][1] for l in E_LAYERS]
    ta = [dd2[f"table_only{l}"][1] for l in E_LAYERS]
    lines.append(f"- P-e calm-vs-table single-layer dLoop profile "
                 f"Spearman {_spearman(ca, ta):+.3f} (descriptive, n=8)")

    (OUT / "report.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "run1"
    if what == "run1":
        run1()
    elif what == "run2":
        run2()
    elif what == "analyze":
        analyze()
    print("DONE", flush=True)
