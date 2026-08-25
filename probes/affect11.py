"""affect-11 — closure-formula vs settled-state (the grouping-axis
adjudication). Prereg: results/affect11-prereg.md (frozen before run).

The affect-08 residue: per-emotion turn-end potency is dose-stable and
NOT circumplex-ordered (anger/pride at floor, calm saturating).
PREDICTIONS.md's settled-pole demotion already names the mechanical
candidate — "trained closure formulas, not a settled state". This run
puts closure-register LENS directions (W_U[t] @ J_l, single tokens,
AffectSteer norm convention -> magnitude-matched to the emotion
injections by construction) into the affect-07/08 pulse harness against
matched mundane tokens and the pure exit-token direction, and dumps the
geometry needed to correlate all 40 measured affect-08 potencies with
closure/exit alignment.

Usage:
  .venv/bin/python probes/affect11.py run
  .venv/bin/python probes/affect11.py analyze
"""

import json
import sys

import torch

from lab import RESULTS, Steering, get_model
from affect2 import _load_vectors
from affect3 import AffectSteer, E_LAYERS
from concepts import outdir as a6dir
from fanout import TYPO
from loops import loop_gram
from affect7 import (CFG, PRE, PULSE, POST, WINDOW, N_STEER,
                     _exit_id, _prompt_ids, _sample, _events)

MODEL = "qwen-27b"
AE = 0.08
SEEDS = list(range(8))
CLOSURE = [" goodbye", " farewell", " conclusion", " finished",
           " Thanks", " ending"]
MUNDANE = [" table", " garden", " metal", " window", " cotton",
           " engine"]
OUT = RESULTS / "affect11-q27b"


def _pullback(lm, token_strs, extra_ids=()):
    """[n, n_layers, d] lens-pullback directions at E_LAYERS (zeros
    elsewhere; AffectSteer only indexes the layers it is given)."""
    W = lm.model._lm_head.weight.detach()
    n_layers = len(lm.model.layers)
    tids = []
    for w in token_strs:
        ids = lm.tok(w, add_special_tokens=False).input_ids
        assert len(ids) == 1, (w, ids)
        tids.append(ids[0])
    tids += list(extra_ids)
    V = torch.zeros(len(tids), n_layers, W.shape[1])
    for l in E_LAYERS:
        assert l in lm.lens.jacobians, f"no jacobian at L{l}"
        J = lm.lens.jacobians[l].to(W.device)
        for i, t in enumerate(tids):
            v = (W[t].float() @ J).cpu()
            V[i, l] = v / v.norm()
    return V


def _cos_profile(A, B, layers):
    """mean over layers of cos(A[l], B[l]) for unit-normalized rows."""
    cs = []
    for l in layers:
        a = A[l] / A[l].norm()
        b = B[l] / B[l].norm()
        cs.append(float(a @ b))
    return sum(cs) / len(cs)


def run() -> None:
    cfg = CFG[MODEL]
    OUT.mkdir(parents=True, exist_ok=True)
    lm = get_model(MODEL)
    ids = _prompt_ids(lm, MODEL)
    im_end = _exit_id(lm, MODEL)

    # --- directions ---------------------------------------------------
    Vtok = _pullback(lm, CLOSURE + MUNDANE, extra_ids=[im_end])
    Vemo, emos = _load_vectors(MODEL)
    cv = torch.load(a6dir(MODEL) / "cvectors.pt")
    Vcon, slugs = cv["anthropic"], cv["slugs"]

    # --- geometry dump (prereg P-iii; no generation cost) -------------
    exit_prof = Vtok[len(CLOSURE) + len(MUNDANE)]     # [n_layers, d]
    clo_mean = Vtok[:len(CLOSURE)].mean(0)
    geom = {"e_layers": E_LAYERS, "cos_exit": {}, "cos_closure": {}}
    for name, prof in (
            [(e, Vemo[i]) for i, e in enumerate(emos)]
            + [(s, Vcon[j]) for j, s in enumerate(slugs)]
            + [(w.strip(), Vtok[k])
               for k, w in enumerate(CLOSURE + MUNDANE)]):
        geom["cos_exit"][name] = round(
            _cos_profile(prof, exit_prof, E_LAYERS), 4)
        geom["cos_closure"][name] = round(
            _cos_profile(prof, clo_mean, E_LAYERS), 4)
    (OUT / "geometry.json").write_text(json.dumps(geom, indent=1))
    print("geometry dumped", flush=True)

    # --- forced loop (affect-08 convention, greedy => reproducible) ---
    with Steering(lm, TYPO, cfg["mid"], "amplify",
                  cfg["alpha_typo"]), torch.no_grad():
        forced = lm.model._hf_model.generate(
            ids, max_new_tokens=N_STEER, do_sample=False)
    ftext = lm.tok.decode(forced[0, ids.shape[1]:], skip_special_tokens=True)
    g1, n1 = loop_gram(ftext)
    lw = (g1.split()[0] if g1 else "luckily").lower()
    print(f"forced loop4={g1!r}x{n1} loopword={lw!r}", flush=True)

    conds = [("none", "none", None)]
    conds.append(("calm", "emotion",
                  lambda: AffectSteer(lm, Vemo, emos.index("calm"),
                                      E_LAYERS, "amplify", AE)))
    conds.append(("tall", "concept",
                  lambda: AffectSteer(lm, Vcon, slugs.index("tall"),
                                      E_LAYERS, "amplify", AE)))
    conds.append(("exitdir", "exitdir",
                  lambda: AffectSteer(lm, Vtok,
                                      len(CLOSURE) + len(MUNDANE),
                                      E_LAYERS, "amplify", AE)))
    for k, w in enumerate(CLOSURE):
        conds.append((w.strip(), "closure",
                      (lambda k=k: AffectSteer(lm, Vtok, k, E_LAYERS,
                                               "amplify", AE))))
    for k, w in enumerate(MUNDANE):
        conds.append((w.strip(), "mundane",
                      (lambda k=k: AffectSteer(lm, Vtok,
                                               len(CLOSURE) + k,
                                               E_LAYERS, "amplify",
                                               AE))))
    print(f"{len(conds)} conditions x {len(SEEDS)} seeds @ ae={AE}",
          flush=True)

    ck = OUT / "affect11.json"
    if ck.exists():
        res = json.loads(ck.read_text())
        assert res["loopword"] == lw, (res["loopword"], lw)
        done = {r["seed"] for r in res["runs"]}
        print(f"resuming: seeds {sorted(done)} complete", flush=True)
    else:
        res = {"model": MODEL, "alpha_e": AE, "e_layers": E_LAYERS,
               "closure": CLOSURE, "mundane": MUNDANE,
               "seeds": SEEDS, "forced_loop4": [g1, n1], "loopword": lw,
               "conditions": [(c[0], c[1]) for c in conds], "runs": []}
        done = set()

    for seed in SEEDS:
        if seed in done:
            continue
        seq1, _ = _sample(lm, forced, PRE, seed=seed)
        if seq1.shape[1] < forced.shape[1] + PRE:
            print(f"  seed {seed}: escaped before pulse — skipped",
                  flush=True)
            continue
        for name, kind, factory in conds:
            ctx = factory() if factory is not None else None
            seq2, _ = _sample(lm, seq1, PULSE, ctx=ctx, seed=seed + 10_000)
            if seq2.shape[1] < seq1.shape[1] + PULSE:
                seq3 = seq2
            else:
                seq3, _ = _sample(lm, seq2, POST, seed=seed + 20_000)
            free = seq3[0, forced.shape[1]:]
            toks = [lm.tok.decode([int(t)]) for t in free]
            exited = len(free) < PRE + PULSE + POST
            exit_step = len(free) if exited else None
            res["runs"].append({
                "seed": seed, "cond": name, "kind": kind,
                "n_steps": len(free),
                "deloop_step": _events(toks, lw, PRE),
                "exited": exited, "exit_step": exit_step,
                "turnend_in_window": bool(
                    exit_step is not None
                    and PRE <= exit_step < PRE + WINDOW),
                "loop_frac_post": round(
                    sum(lw in t.lower() for t in toks[PRE:])
                    / max(1, len(toks) - PRE), 3),
                "text_tail": "".join(toks)[-80:]})
            r = res["runs"][-1]
            print(f"  s{seed} {name:<12} exit={exit_step} "
                  f"turnend@W={r['turnend_in_window']} "
                  f"lf={r['loop_frac_post']}", flush=True)
        (OUT / "affect11.json").write_text(json.dumps(res, indent=1))
    print("RUN DONE", flush=True)


def analyze() -> None:
    import itertools
    import random as _random
    res = json.loads((OUT / "affect11.json").read_text())
    geom = json.loads((OUT / "geometry.json").read_text())
    runs = res["runs"]
    kind = dict(res["conditions"])

    def te(name):
        rs = [r for r in runs if r["cond"] == name]
        return sum(r["turnend_in_window"] for r in rs) / len(rs)

    names = sorted({r["cond"] for r in runs}, key=lambda n: -te(n))
    lines = [f"# affect-11 (qwen-27b, ae={res['alpha_e']}) — "
             "closure-formula vs settled-state", "",
             "| cond | kind | turnend@W |", "|---|---|---|"]
    for n in names:
        lines.append(f"| {n} | {kind[n]} | {te(n):.3f} |")

    clo = [n for n in names if kind[n] == "closure"]
    mun = [n for n in names if kind[n] == "mundane"]
    cm, mm = (sum(te(n) for n in clo) / len(clo),
              sum(te(n) for n in mun) / len(mun))
    lines += ["", "## P-i closure vs mundane (direction-level, exact)",
              f"- closure mean {cm:.3f}, mundane mean {mm:.3f}, "
              f"gap {cm - mm:+.3f}"]
    scores = [te(n) for n in clo + mun]
    obs = cm - mm
    ge = tot = 0
    for pick in itertools.combinations(range(12), 6):
        a = sum(scores[i] for i in pick) / 6
        b = (sum(scores) - sum(scores[i] for i in pick)) / 6
        tot += 1
        if abs(a - b) >= abs(obs) - 1e-12:
            ge += 1
    lines.append(f"- exact permutation over {tot} labellings: "
                 f"p={ge / tot:.4f}"
                 f"{' (sig .05)' if ge / tot < .05 else ''}")
    lines += ["", "## P-ii exitdir / anchors",
              f"- exitdir {te('exitdir'):.3f}  calm {te('calm'):.3f}  "
              f"tall {te('tall'):.3f}  none {te('none'):.3f}"]

    # P-iii: correlate affect-08 measured potency with alignment
    def a8(path):
        d = json.loads((RESULTS / path / "affect08.json").read_text())
        out = {}
        for c in {r["cond"] for r in d["runs"]}:
            rs = [r for r in d["runs"] if r["cond"] == c]
            out[c] = sum(r["turnend_in_window"] for r in rs) / len(rs)
        return out
    p1, p2 = a8("affect08-q27b-ae08"), a8("affect08-q27b-ae1")
    dirs = [n for n in geom["cos_exit"]
            if n in p1 and n in p2 and n != "none"]
    pot = {n: (p1[n] + p2[n]) / 2 for n in dirs}

    def spearman(x, y):
        def rank(v):
            s = sorted(range(len(v)), key=lambda i: v[i])
            r = [0.0] * len(v)
            for i, j in enumerate(s):
                r[j] = i
            return r
        rx, ry = rank(x), rank(y)
        n = len(x)
        mx = sum(rx) / n
        my = sum(ry) / n
        num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
        den = (sum((a - mx) ** 2 for a in rx)
               * sum((b - my) ** 2 for b in ry)) ** 0.5
        return num / den if den else 0.0

    lines += ["", f"## P-iii potency (affect-08 both doses, n={len(dirs)}"
              ") vs alignment"]
    rng = _random.Random(2718)
    for key in ("cos_exit", "cos_closure"):
        xs = [geom[key][n] for n in dirs]
        ys = [pot[n] for n in dirs]
        rho = spearman(xs, ys)
        ge = 0
        N = 20000
        for _ in range(N):
            sh = ys[:]
            rng.shuffle(sh)
            if abs(spearman(xs, sh)) >= abs(rho) - 1e-12:
                ge += 1
        lines.append(f"- {key}: rho {rho:+.3f}, permutation "
                     f"p={ge / N:.4f}"
                     f"{' (sig .05)' if ge / N < .05 else ''}")

    (OUT / "report.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "run"
    if what == "run":
        run()
    elif what == "analyze":
        analyze()
    print("DONE", flush=True)
