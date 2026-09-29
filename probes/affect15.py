"""affect-15 — is band cooperation a coalition or a dose law?
Dose-matched fewer-layer injections vs full-stack, in chunks.
Prereg: results/affect15-prereg.md (frozen before run). Reuses the
affect-13/14 raw-logit trace machinery.

Usage:
  .venv/bin/python probes/affect15.py run A|B|C
  .venv/bin/python probes/affect15.py analyze A|B|C
"""

import json
import math
import random
import sys

import torch

from lab import RESULTS, get_model
from affect2 import _load_vectors
from affect3 import AffectSteer, E_LAYERS
from affect7 import PRE, PULSE, POST, WINDOW, _exit_id, _prompt_ids
from affect11 import _pullback
from affect13 import _sample_raw, _trace
from affect14 import _forced

MODEL = "qwen-27b"
AE = 0.08
SEEDS = list(range(16, 28))
OUT = RESULTS / "affect15-q27b"
SETS = {"full": E_LAYERS, "k4s": [28, 36, 44, 52], "k2s": [36, 52],
        "k1": [44], "k4c": [36, 40, 44, 48], "k2c": [40, 44],
        "k1_32": [32], "k1_52": [52], "k6s": [28, 32, 40, 44, 52, 56],
        "k1_28": [28], "k1_36": [36], "k1_56": [56]}
CHUNKS = {
    "A": [("calm", "full", .08), ("calm", "full", .04),
          ("calm", "full", .02), ("calm", "k1", "m"),
          ("calm", "k2s", "m"), ("calm", "k4s", "m"),
          ("calm", "k4s", .08), ("calm", "k2s", .08),
          ("rand1", "full", .08), ("rand1", "k1", "m"),
          ("rand1", "k4s", "m")],
    "B": [(d, s, a) for d in ("proud", "reflective", "table")
          for s, a in (("full", .08), ("full", .04), ("k4s", "m"),
                       ("k1", "m"))],
    "C": [("calm", "full", .12), ("calm", "k1_32", "m"),
          ("calm", "k1_52", "m"), ("calm", "k2c", "m"),
          ("calm", "k4c", "m"), ("calm", "k4c", .08),
          ("calm", "k6s", .08), ("rand2", "k1", "m"),
          ("rand2", "k4s", "m")],
    "D": [("calm", s, .64) for s in ("k1_28", "k1_36", "k1", "k1_52",
                                     "k1_56")]
    + [("calm", "full", .06), ("calm", "full", .10),
       ("rand1", "k1_28", .64), ("rand2", "k1_52", .64)],
}


def cname(d, s, a):
    return f"{d}_{s}@{a if a == 'm' else f'{a:.2f}'}"


def _norms(lm, forced):
    """Mean residual norm at each hooked layer output, last 20 positions
    of the forced loop (hidden_states[l + 1] = output of block l)."""
    with torch.no_grad():
        hs = lm.model._hf_model(forced, output_hidden_states=True
                                ).hidden_states
    return {l: float(hs[l + 1][0, -20:].float().norm(dim=-1).mean())
            for l in E_LAYERS}


def _alpha(a, layers, norms):
    if a != "m":
        return a
    return AE * sum(norms[l] for l in E_LAYERS) / sum(norms[l]
                                                       for l in layers)


def _ctx(lm, Vemo, emos, Vtok, d, layers, alpha):
    if d == "table":
        return lambda: AffectSteer(lm, Vtok, 0, layers, "amplify", alpha)
    if d.startswith("rand"):
        r = int(d[4:])
        return lambda: AffectSteer(lm, Vemo, 0, layers, "amplify", alpha,
                                   rand_seed=r)
    i = emos.index(d)
    return lambda: AffectSteer(lm, Vemo, i, layers, "amplify", alpha)


def run(chunk) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    lm = get_model(MODEL)
    ids = _prompt_ids(lm, MODEL)
    exit_id = _exit_id(lm, MODEL)
    Vemo, emos = _load_vectors(MODEL)
    Vtok = _pullback(lm, [" table"], extra_ids=[exit_id])
    forced, g1, n1, lw, loop_id = _forced(lm, ids)
    norms = _norms(lm, forced)
    print("norms", {l: round(v, 1) for l, v in norms.items()}, flush=True)

    conds = [("none", None, None, None)]
    for d, s, a in CHUNKS[chunk]:
        layers = SETS[s]
        alpha = _alpha(a, layers, norms)
        conds.append((cname(d, s, a), layers, alpha,
                      _ctx(lm, Vemo, emos, Vtok, d, layers, alpha)))
    meta = {"model": MODEL, "chunk": chunk, "alpha_e": AE,
            "e_layers": E_LAYERS, "forced_loop4": [g1, n1],
            "loopword": lw, "loop_id": loop_id, "exit_id": exit_id,
            "pre": PRE, "pulse": PULSE, "post": POST, "window": WINDOW,
            "norms": {str(l): v for l, v in norms.items()}}

    ck = OUT / f"affect15-{chunk}.json"
    if ck.exists():
        res = json.loads(ck.read_text())
        assert res["loopword"] == lw
        done = {r["seed"] for r in res["runs"]}
        print(f"{chunk}: resuming, seeds {sorted(done)} complete",
              flush=True)
    else:
        res = dict(meta)
        res.update({"conditions": [
            {"name": n, "layers": L, "alpha": al,
             "abs_dose": (al * sum(norms[l] for l in L)) if L else 0.0}
            for n, L, al, _ in conds], "seeds": SEEDS, "runs": []})
        done = set()
    print(f"chunk {chunk}: {len(conds)} conds x {len(SEEDS)} seeds",
          flush=True)
    for c in res["conditions"]:
        print(f"  {c['name']:<22} alpha={c['alpha']} "
              f"abs_dose={c['abs_dose']:.1f}", flush=True)

    for seed in SEEDS:
        if seed in done:
            continue
        seq1, lg1 = _sample_raw(lm, forced, PRE, seed=seed)
        if seq1.shape[1] < forced.shape[1] + PRE:
            print(f"  seed {seed}: escaped before pulse — skipped",
                  flush=True)
            continue
        tr1 = _trace(lg1, exit_id, loop_id)
        for name, _, _, factory in conds:
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
            n_free = seq3.shape[1] - forced.shape[1]
            exited = n_free < PRE + PULSE + POST
            exit_step = n_free if exited else None
            res["runs"].append({
                "seed": seed, "cond": name, "n_steps": n_free,
                "exited": exited, "exit_step": exit_step,
                "turnend_in_window": bool(
                    exit_step is not None
                    and PRE <= exit_step < PRE + WINDOW),
                "text": lm.tok.decode(seq3[0, forced.shape[1]:],
                                      skip_special_tokens=False),
                "trace": tr1 + tr2 + tr3})
            print(f"  [{chunk}] s{seed} {name:<22} exit={exit_step}",
                  flush=True)
        ck.write_text(json.dumps(res))
    print(f"chunk {chunk} DONE", flush=True)


# ------------------------------------------------------------ analysis
def _per_seed(res):
    """{cond: {seed: (dExit, dLoop)}} — mean over pulse steps vs none."""
    pre, pulse = res["pre"], res["pulse"]
    none = {r["seed"]: r["trace"] for r in res["runs"]
            if r["cond"] == "none"}
    out = {}
    for r in res["runs"]:
        if r["cond"] == "none" or r["seed"] not in none:
            continue
        nt = none[r["seed"]]
        idx = range(pre, min(pre + pulse, len(r["trace"]), len(nt)))
        if not idx:
            continue
        de = sum(r["trace"][t][0] - nt[t][0] for t in idx) / len(idx)
        dl = sum(r["trace"][t][1] - nt[t][1] for t in idx) / len(idx)
        out.setdefault(r["cond"], {})[r["seed"]] = (de, dl)
    return out


def _mean(ps, cond, seeds, k):
    v = [ps[cond][s][k] for s in seeds if s in ps[cond]]
    return sum(v) / len(v)


def _ratio_ci(ps, num, den, seeds, rng, n=2000):
    vals = []
    for _ in range(n):
        bs = [rng.choice(seeds) for _ in seeds]
        d = _mean(ps, den, bs, 1)
        if d:
            vals.append(_mean(ps, num, bs, 1) / d)
    vals.sort()
    return vals[int(.025 * len(vals))], vals[int(.975 * len(vals)) - 1]


def _load(chunk):
    return json.loads((OUT / f"affect15-{chunk}.json").read_text())


def _table(res, ps):
    seeds = sorted({r["seed"] for r in res["runs"]})
    te = {}
    for r in res["runs"]:
        te.setdefault(r["cond"], []).append(r["turnend_in_window"])
    lines = ["| cond | alpha | Σα‖h‖ | dExit | dLoop | dMargin | "
             "turn-end |", "|---|---|---|---|---|---|---|"]
    for c in res["conditions"]:
        n = c["name"]
        t = sum(te[n]) / len(te[n])
        if n == "none":
            lines.append(f"| none | — | 0 | — | — | — | {t:.2f} |")
            continue
        de, dl = _mean(ps, n, seeds, 0), _mean(ps, n, seeds, 1)
        lines.append(f"| {n} | {c['alpha']:.3f} | {c['abs_dose']:.1f} | "
                     f"{de:+.2f} | {dl:+.2f} | {de - dl:+.2f} | {t:.2f} |")
    return seeds, lines


def _determinism(res):
    """none + calm full@.08 vs affect-14 Part 1 (same seeds, same CRN)."""
    p1 = RESULTS / "affect14-q27b" / "affect14-part1.json"
    if not p1.exists():
        return "affect-14 part1 missing"
    old = json.loads(p1.read_text())
    pairs = (("none", "none"), ("calm_full@0.08", "calm"))
    worst, n = 0.0, 0
    for new_c, old_c in pairs:
        o = {r["seed"]: r["trace"] for r in old["runs"]
             if r["cond"] == old_c}
        for r in res["runs"]:
            if r["cond"] != new_c or r["seed"] not in o:
                continue
            a, b = r["trace"], o[r["seed"]]
            for t in range(min(len(a), len(b))):
                worst = max(worst, abs(a[t][0] - b[t][0]),
                            abs(a[t][1] - b[t][1]))
            n += 1
    return f"max |Δlogit| vs affect-14 part1 over {n} runs: {worst:.3f}"


def _full08():
    r = _load("A")
    ps = _per_seed(r)
    return _mean(ps, "calm_full@0.08",
                 sorted({x["seed"] for x in r["runs"]}), 1)


def analyze(chunk) -> None:
    rng = random.Random(1515)
    res = _load(chunk)
    ps = _per_seed(res)
    seeds, lines = _table(res, ps)
    head = [f"# affect-15 chunk {chunk} (qwen-27b, {len(seeds)} seeds)",
            "", "norms " + ", ".join(f"L{l} {v:.0f}" for l, v in
                                     res["norms"].items()), ""]
    lines = head + lines + [""]
    m = lambda c: _mean(ps, c, seeds, 1)  # noqa: E731
    mg = lambda c: _mean(ps, c, seeds, 0) - m(c)  # noqa: E731

    if chunk == "A":
        full = m("calm_full@0.08")
        R = {k: m(f"calm_{k}@m") / full for k in ("k1", "k2s", "k4s")}
        ci = {k: _ratio_ci(ps, f"calm_{k}@m", "calm_full@0.08", seeds,
                           rng) for k in ("k1", "k4s")}
        if R["k4s"] >= .6 and R["k1"] >= .5:
            v = "DOSE"
        elif R["k4s"] <= .35 and R["k1"] <= .25:
            v = "COALITION"
        else:
            v = "GRADED"
        lines += [f"- **V1** R1 = {R['k1']:+.2f} "
                  f"[{ci['k1'][0]:+.2f}, {ci['k1'][1]:+.2f}], "
                  f"R2 = {R['k2s']:+.2f}, R4 = {R['k4s']:+.2f} "
                  f"[{ci['k4s'][0]:+.2f}, {ci['k4s'][1]:+.2f}] → **{v}**"]
        generic = False
        for k in ("k1", "k4s"):
            fr = m(f"rand1_{k}@m") / m(f"calm_{k}@m")
            generic |= fr >= .5
            lines.append(f"- **V2** {k}@m: rand1 dLoop = {fr:+.0%} of "
                         f"calm's; calm − rand1 dMargin "
                         f"{mg(f'calm_{k}@m') - mg(f'rand1_{k}@m'):+.2f}")
        if v == "DOSE" and generic:
            lines.append("- **V2 flag: GENERIC** — concentrated push "
                         "breaks the loop regardless of direction")
        g4 = abs(m("calm_k4s@0.08") - m("calm_full@0.04")) / abs(full)
        g2 = abs(m("calm_k2s@0.08") - m("calm_full@0.02")) / abs(full)
        lines += [f"- **V3** gap4 = {g4:.2f}, gap2 = {g2:.2f} "
                  f"(H-D predicts ≤ 0.25) → "
                  f"{'PASS' if max(g4, g2) <= .25 else 'FAIL'}",
                  f"- exponent check: full@.04 = "
                  f"{m('calm_full@0.04') / full:.0%}, full@.02 = "
                  f"{m('calm_full@0.02') / full:.0%} of full@.08 "
                  f"(affect-14 fit predicts ~22% / ~5%)",
                  f"- determinism: {_determinism(res)}"]
    elif chunk == "B":
        for d in ("proud", "reflective", "table"):
            full = m(f"{d}_full@0.08")
            r1, r4 = m(f"{d}_k1@m") / full, m(f"{d}_k4s@m") / full
            v = ("DOSE" if r4 >= .6 and r1 >= .5 else "COALITION"
                 if r4 <= .35 and r1 <= .25 else "GRADED")
            lines.append(f"- {d}: full dLoop {full:+.2f}, R1 {r1:+.2f}, "
                         f"R4 {r4:+.2f}, half-dose "
                         f"{m(f'{d}_full@0.04') / full:.0%} → {v}")
    elif chunk == "C":
        allc = {}
        for ch in ("A", "C"):
            p = OUT / f"affect15-{ch}.json"
            if not p.exists():
                continue
            r_ = json.loads(p.read_text())
            ps_ = _per_seed(r_)
            sd = sorted({r["seed"] for r in r_["runs"]})
            for c in r_["conditions"]:
                if c["name"].startswith("calm"):
                    allc[c["name"]] = (c["abs_dose"],
                                       _mean(ps_, c["name"], sd, 1))
        full = allc["calm_full@0.08"][1]
        ladder = [allc[f"calm_full@{a:.2f}"] for a in (.02, .04, .08, .12)
                  if f"calm_full@{a:.2f}" in allc]
        xs = [math.log(d) for d, y in ladder if y < 0]
        ys = [math.log(-y) for d, y in ladder if y < 0]
        mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
        b = (sum((x - mx) * (y - my) for x, y in zip(xs, ys))
             / sum((x - mx) ** 2 for x in xs))
        a0 = my - b * mx
        lines += [f"- dose-alone model: |dLoop| = e^{a0:.2f} · D^{b:.2f} "
                  f"(fit on full-stack ladder, n={len(xs)})", "",
                  "| calm arm | D | obs frac | pred frac | miss |",
                  "|---|---|---|---|---|"]
        misses = []
        for n, (d, y) in sorted(allc.items(), key=lambda kv: kv[1][0]):
            pred = -math.exp(a0 + b * math.log(d))
            miss = (y - pred) / full
            if abs(miss) > .25:
                misses.append(n)
            lines.append(f"| {n} | {d:.1f} | {y / full:+.2f} | "
                         f"{pred / full:+.2f} | {miss:+.2f} |")
        lines += ["", f"- H-D dose-alone: "
                  f"{'PASS' if not misses else 'FAIL'}"
                  f"{' — misses: ' + ', '.join(misses) if misses else ''}"]
        for k in ("k1", "k4s"):
            lines.append(f"- rand2 {k}@m dLoop {m(f'rand2_{k}@m'):+.2f}, "
                         f"dMargin {mg(f'rand2_{k}@m'):+.2f}")

    elif chunk == "D":
        full = _full08()
        fr = {s: m(f"calm_{s}@0.64") / full
              for s in ("k1_28", "k1_36", "k1", "k1_52", "k1_56")}
        hr = all(.65 <= v <= 1.35 for v in fr.values())
        hp = (fr["k1_28"] + fr["k1_36"]) / 2 - (fr["k1_52"]
                                                 + fr["k1_56"]) / 2
        lines += ["- single layer at α .64, dLoop as fraction of "
                  "full@.08 (chunk A): " + ", ".join(
                      f"{s} {v:+.2f}" for s, v in fr.items()),
                  f"- **H-R** (all in [0.65, 1.35]): "
                  f"{'PASS' if hr else 'FAIL'}",
                  f"- **H-P** (early − late = {hp:+.2f}, bar > 0.5): "
                  f"{'PASS' if hp > .5 else 'FAIL'}"]
        for d, s in (("rand1", "k1_28"), ("rand2", "k1_52")):
            lines.append(f"- {d} {s}@.64 dMargin {mg(f'{d}_{s}@0.64'):+.2f}"
                         f" vs calm {mg(f'calm_{s}@0.64'):+.2f}")
        lines.append(f"- threshold shape: full@.06 "
                     f"{m('calm_full@0.06') / full:+.2f}, full@.10 "
                     f"{m('calm_full@0.10') / full:+.2f}")

    (OUT / f"report-{chunk}.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    what, chunk = sys.argv[1], sys.argv[2]
    assert chunk in CHUNKS
    run(chunk) if what == "run" else analyze(chunk)
    print("DONE", flush=True)
