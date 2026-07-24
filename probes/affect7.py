"""affect-07 — does AFFECT break the loop, or does MEANING? (P18)

The causal affect arm (affect-03: emotion state gates the turn-end exit;
affect-04: family-scaled emotion escape on gemma-12b) rests entirely on
matched-RANDOM controls, which test perturbation magnitude and nothing
else. affect-04's own leading reading is the deflation: *any* meaningful
on-manifold direction might disrupt a marginal loop coalition. This run
puts a matched set of meaningful NON-AFFECTIVE directions (affect-06,
built by the identical pipeline) into the same lever and asks which
account survives.

Preregistered as P18 before the run. Three nested accounts:
  H0 norm     — emotions ~ concepts ~ randoms          (already dead)
  H1 manifold — emotions ~ concepts >> randoms, no valence ordering
  H2 affect   — emotions beyond the concept null AND escape tracks
                valence across the roster; concepts scatter about zero

Design. qwen-27b pinned at alpha_typo = 0.65 — the LOCKED shelf of the
affect-05 sampled-hazard cliff (8/8 seeds x 300 steps, loopfrac 1.00),
which fixes affect-05's fatal problem: spontaneous escapes there were
too fast to window, here the baseline hazard is ~0 and any effect is
visible against a clean floor.

Per seed:
  phase 1  free steps 0-19, UNSTEERED, sampled      -> shared context
  phase 2  free steps 20-29, ONE direction injected -> the pulse
  phase 3  free steps 30-79, UNSTEERED, sampled     -> does it escape?

Phase 1 is computed ONCE per seed and shared by every condition, and
phases 2/3 re-seed the RNG identically per condition (common random
numbers). So conditions differ only in the injected direction: same
loop, same sampling noise, paired comparison.

Pulse convention (stated because it matters): the hook is active for
the whole forward pass of phase 2, i.e. at all positions including the
recomputed prefix — identical to the free-phase steering convention of
affect-03/04, and identical across every condition, so the comparison
is fair. It is "steering on during a 10-step window", not "steering the
10 new positions only".

Primary endpoint: escape (deloop or turn-end) within 20 steps of pulse
onset. Secondary: im_end logit lift during the pulse, top1-top2 margin.

Output: results/affect07-q27b/{affect07.json, report.md}
Usage:  .venv/bin/python probes/affect7.py [run|analyze|both]
"""

import json
import sys

import torch

from lab import CONFIGS, RESULTS, Steering, _strip_bos, get_model
from affect import EMOTIONS
from affect2 import _load_vectors
from affect3 import AffectSteer, E_LAYERS
from affect4 import E_LAYERS_G12B, MID_G12B
from concepts import outdir as a6dir
from fanout import TYPO, WATER
from loops import loop_gram

# Per-family constants. qwen: the affect-05 locked shelf. gemma-12b: the
# affect-04b substrate (8-11x its alpha*) at the dose inside the narrow
# specificity window 0.004 < ceiling < 0.008.
CFG = {
    "qwen-27b": {
        "mid": [28, 32, 36, 40], "alpha_typo": 0.65,
        "e_layers": E_LAYERS, "alpha_e": 0.12,
        "exit_token": "<|im_end|>", "tag": "q27b"},
    "gemma-12b": {
        "mid": MID_G12B, "alpha_typo": 0.12,
        "e_layers": E_LAYERS_G12B, "alpha_e": 0.004,
        "exit_token": "<end_of_turn>", "tag": "g12b"},
}

N_STEER = 50               # forced phase, greedy, identical for all
PRE, PULSE, POST = 20, 10, 50      # free-phase step budget
WINDOW = 20                # escape window from pulse onset
TEMP = 1.0                 # top-k / top-p inherited (affect-05 note)
SEEDS = list(range(8))

POS = ["calm", "content", "happy", "grateful", "hopeful", "blissful"]
NEG = ["desperate", "distressed", "anxious", "afraid", "sad", "angry"]


def outdir(model: str):
    d = RESULTS / f"affect07-{CFG[model]['tag']}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _prompt_ids(lm, model: str):
    tkw = CONFIGS[model].get("template_kwargs", {})
    prefix = _strip_bos(lm.tok, lm.tok.apply_chat_template(
        [{"role": "user", "content": WATER}], tokenize=False,
        add_generation_prompt=True, **tkw))
    return lm.model.encode(prefix, max_length=1_000_000)


def _exit_id(lm, model: str) -> int:
    i = lm.tok.convert_tokens_to_ids(CFG[model]["exit_token"])
    return i if i is not None and i >= 0 else lm.tok.eos_token_id


def _sample(lm, ids, n, ctx=None, seed=None):
    """One sampled continuation; returns (sequences, scores list)."""
    if seed is not None:
        torch.manual_seed(seed)
    mgr = ctx if ctx is not None else _NoCtx()
    with mgr, torch.no_grad():
        out = lm.model._hf_model.generate(
            ids, max_new_tokens=n, do_sample=True, temperature=TEMP,
            output_scores=True, return_dict_in_generate=True)
    return out.sequences, list(out.scores)


class _NoCtx:
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _conditions(lm, model: str):
    """[(name, kind, factory-or-None, valence)] — None = no pulse."""
    lay, ae = CFG[model]["e_layers"], CFG[model]["alpha_e"]
    V, emos = _load_vectors(model)                    # [E, L, D]
    cv = torch.load(a6dir(model) / "cvectors.pt")
    C, slugs = cv["anthropic"], cv["slugs"]           # [C, L, D]
    conds = [("none", "none", None, 0)]
    for e in POS + NEG:
        i = emos.index(e)
        conds.append((e, "emotion",
                      (lambda i=i: AffectSteer(lm, V, i, lay,
                                               "amplify", ae)),
                      EMOTIONS[e]))
    for j, sl in enumerate(slugs):
        conds.append((sl, "concept",
                      (lambda j=j: AffectSteer(lm, C, j, lay,
                                               "amplify", ae)), 0))
    for r in (1, 2):
        conds.append((f"rand{r}", "random",
                      (lambda r=r: AffectSteer(lm, V, 0, lay,
                                               "amplify", ae,
                                               rand_seed=r)), 0))
    return conds


def _events(toks, lw, n_pre):
    """(deloop_step, exit_step) in FREE-phase step coordinates."""
    ind = [lw in t.lower() for t in toks]
    deloop = None
    for t in range(n_pre, len(ind) - 12):
        if not any(ind[t:t + 12]):
            deloop = t
            break
    return deloop


def run(model: str = "qwen-27b") -> None:
    cfg = CFG[model]
    OUT = outdir(model)
    lm = get_model(model)
    ids = _prompt_ids(lm, model)
    im_end = _exit_id(lm, model)

    # ---- forced phase: greedy, identical for every condition ----
    with Steering(lm, TYPO, cfg["mid"], "amplify",
                  cfg["alpha_typo"]), torch.no_grad():
        forced = lm.model._hf_model.generate(
            ids, max_new_tokens=N_STEER, do_sample=False)
    ftext = lm.tok.decode(forced[0, ids.shape[1]:], skip_special_tokens=True)
    g1, n1 = loop_gram(ftext)
    lw = (g1.split()[0] if g1 else "luckily").lower()
    print(f"forced loop4={g1!r}x{n1} loopword={lw!r}", flush=True)

    conds = _conditions(lm, model)
    print(f"{len(conds)} conditions x {len(SEEDS)} seeds", flush=True)
    res = {"model": model, "alpha_typo": cfg["alpha_typo"],
           "mid": cfg["mid"], "e_layers": cfg["e_layers"],
           "alpha_e": cfg["alpha_e"], "temp": TEMP,
           "pre": PRE, "pulse": PULSE, "post": POST, "window": WINDOW,
           "seeds": SEEDS, "forced_loop4": [g1, n1], "loopword": lw,
           "conditions": [(c[0], c[1], c[3]) for c in conds], "runs": []}

    res["seed_baseline"] = {}
    for seed in SEEDS:
        # ---- phase 1: shared, unsteered pre-pulse context ----
        seq1, sc1 = _sample(lm, forced, PRE, seed=seed)
        if seq1.shape[1] < forced.shape[1] + PRE:
            print(f"  seed {seed}: escaped before pulse — skipped",
                  flush=True)
            continue
        # per-seed pre-pulse baselines: the pulse effect is read as a
        # LIFT against these, and they are shared by every condition
        # because phase 1 is byte-identical across conditions.
        b_marg, b_gap = [], []
        for s in sc1:
            f = s[0].float()
            top2 = f.topk(2).values
            b_marg.append(float(top2[0] - top2[1]))
            b_gap.append(float(f[im_end] - f.max()))
        base_marg = sum(b_marg) / len(b_marg)
        base_gap = sum(b_gap) / len(b_gap)
        res["seed_baseline"][str(seed)] = {
            "margin_pre": round(base_marg, 3),
            "imend_gap_pre": round(base_gap, 3)}
        for name, kind, factory, val in conds:
            ctx = factory() if factory is not None else None
            seq2, sc2 = _sample(lm, seq1, PULSE, ctx=ctx,
                                seed=seed + 10_000)
            seq3, sc3 = _sample(lm, seq2, POST, seed=seed + 20_000)
            free = seq3[0, forced.shape[1]:]
            toks = [lm.tok.decode([int(t)]) for t in free]
            scores = sc2 + sc3            # from step PRE onward
            marg, imend_lg = [], []
            for s in scores:
                f = s[0].float()
                top2 = f.topk(2).values
                marg.append(round(float(top2[0] - top2[1]), 3))
                imend_lg.append(round(float(f[im_end]
                                            - f.max()), 3))
            # top-5 at the LAST pulse step: which door, if any, is open?
            # affect-03 found calm makes im_end win outright at 0.68;
            # affect-05 found the sampled escape channel is the contrast
            # pivot ' but'. This records which one the pulse opens.
            fl = scores[PULSE - 1][0].float()
            tv, ti = fl.topk(5)
            top5 = [[lm.tok.decode([int(i)]), round(float(v), 2)]
                    for v, i in zip(tv, ti)]
            deloop = _events(toks, lw, PRE)
            exited = len(free) < PRE + PULSE + POST
            exit_step = len(free) if exited else None
            ev = deloop if deloop is not None else exit_step
            res["runs"].append({
                "seed": seed, "cond": name, "kind": kind,
                "valence": val, "n_steps": len(free),
                "deloop_step": deloop, "exited": exited,
                "exit_step": exit_step, "event_step": ev,
                "escaped_in_window": bool(
                    ev is not None and PRE <= ev < PRE + WINDOW),
                "escaped_ever": bool(ev is not None),
                "loop_frac_post": round(
                    sum(lw in t.lower() for t in toks[PRE:])
                    / max(1, len(toks) - PRE), 3),
                "margin_pulse": round(
                    sum(marg[:PULSE]) / max(1, len(marg[:PULSE])), 3),
                "imend_gap_pulse": round(
                    sum(imend_lg[:PULSE]) / max(1, len(imend_lg[:PULSE])),
                    3),
                "imend_lift": round(
                    sum(imend_lg[:PULSE]) / max(1, len(imend_lg[:PULSE]))
                    - base_gap, 3),
                "margin_lift": round(
                    sum(marg[:PULSE]) / max(1, len(marg[:PULSE]))
                    - base_marg, 3),
                "top5_pulse_end": top5,
                "text_tail": "".join(toks)[-100:]})
            print(f"  s{seed} {name:<12} deloop={deloop} "
                  f"exit={exit_step} win={res['runs'][-1]['escaped_in_window']} "
                  f"lf={res['runs'][-1]['loop_frac_post']}", flush=True)
        (OUT / "affect07.json").write_text(json.dumps(res, indent=1))
    print("RUN DONE", flush=True)


# ------------------------------------------------------------ analysis
def _spearman(x, y):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = rank(x), rank(y)
    n = len(x)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = sum((a - mx) ** 2 for a in rx) ** 0.5
    dy = sum((b - my) ** 2 for b in ry) ** 0.5
    return num / (dx * dy) if dx > 0 and dy > 0 else 0.0


def analyze(model: str = "qwen-27b") -> None:
    OUT = outdir(model)
    res = json.loads((OUT / "affect07.json").read_text())
    runs = res["runs"]
    names = [c[0] for c in res["conditions"]]
    kind = {c[0]: c[1] for c in res["conditions"]}
    val = {c[0]: c[2] for c in res["conditions"]}

    def agg(name, key):
        rs = [r for r in runs if r["cond"] == name]
        return (sum(float(r[key]) for r in rs) / len(rs)) if rs else 0.0

    esc = {n: agg(n, "escaped_in_window") for n in names}
    ever = {n: agg(n, "escaped_ever") for n in names}
    lf = {n: agg(n, "loop_frac_post") for n in names}
    ie = {n: agg(n, "imend_lift") for n in names}
    base = esc.get("none", 0.0)

    lines = [f"# affect-07 — affect vs meaning ({res['model']})",
             "", f"alpha_typo {res['alpha_typo']}, alpha_e "
             f"{res['alpha_e']}, layers {res['e_layers']}, "
             f"{len(res['seeds'])} seeds, pulse steps "
             f"{res['pre']}-{res['pre'] + res['pulse']}, "
             f"window {res['window']}", "",
             f"forced loop: {res['forced_loop4']}, loopword "
             f"{res['loopword']!r}", "",
             "## Per-condition (primary = escape@window; secondary = "
             "exit-token lift vs the shared per-seed pre-pulse baseline)",
             "",
             "| condition | kind | valence | escape@window | escape@ever "
             "| loopfrac post | exit lift |",
             "|---|---|---|---|---|---|---|"]
    for n in sorted(names, key=lambda n: (-esc[n], -ie[n], n)):
        lines.append(f"| {n} | {kind[n]} | {val[n]:+d} | {esc[n]:.2f} | "
                     f"{ever[n]:.2f} | {lf[n]:.2f} | {ie[n]:+.3f} |")

    emo = [n for n in names if kind[n] == "emotion"]
    con = [n for n in names if kind[n] == "concept"]
    rnd = [n for n in names if kind[n] == "random"]

    def mean(xs):
        return sum(xs) / len(xs) if xs else 0.0

    import itertools
    lines += ["", "## P18 decision", "",
              f"baseline (no pulse): escape@window {base:.2f}, "
              f"loopfrac post {lf.get('none', 0):.2f}", ""]

    for label, ep, fmt in (("PRIMARY escape@window", esc, "{:.3f}"),
                           ("SECONDARY exit-token lift", ie, "{:+.3f}")):
        cvals = sorted(ep[n] for n in con)
        p95 = (cvals[min(len(cvals) - 1, int(0.95 * len(cvals)))]
               if cvals else 0.0)
        above = [n for n in emo if ep[n] > p95]
        lines += [f"### {label}", "",
                  f"- emotions n={len(emo)}  mean "
                  f"{fmt.format(mean([ep[n] for n in emo]))}  max "
                  f"{fmt.format(max([ep[n] for n in emo], default=0))}",
                  f"- concepts n={len(con)}  mean "
                  f"{fmt.format(mean([ep[n] for n in con]))}  max "
                  f"{fmt.format(max([ep[n] for n in con], default=0))}"
                  f"  95th pct {fmt.format(p95)}",
                  f"- randoms  n={len(rnd)}  mean "
                  f"{fmt.format(mean([ep[n] for n in rnd]))}",
                  f"- emotions above the concept 95th pct: "
                  f"{above if above else 'none'}"]
        rho = _spearman([val[n] for n in emo], [ep[n] for n in emo])
        lines += [f"- valence ordering across emotions: Spearman rho "
                  f"{rho:+.3f} (positive = positive valence scores "
                  f"higher — the affect-03 calm-grants sign)",
                  f"  - pos-valence mean "
                  f"{fmt.format(mean([ep[n] for n in emo if val[n] > 0]))}"
                  f" vs neg-valence mean "
                  f"{fmt.format(mean([ep[n] for n in emo if val[n] < 0]))}"]
        # pseudo-valence null: any balanced +-1 labelling of the concept
        # roster is arbitrary, so the spread of |rho| over many such
        # labellings is the null the emotion |rho| must beat.
        cs = [ep[n] for n in con]
        half = len(cs) // 2
        rhos = sorted(
            abs(_spearman([1 if i in set(c) else -1
                           for i in range(len(cs))], cs))
            for c in itertools.islice(
                itertools.combinations(range(len(cs)), half), 2000))
        q95 = rhos[int(0.95 * len(rhos))] if rhos else 0.0
        lines += [f"- concept pseudo-valence null: |rho| 95th pct "
                  f"{q95:.3f} over {len(rhos)} balanced labellings; "
                  f"observed emotion |rho| {abs(rho):.3f} -> "
                  f"{'BEATS null' if abs(rho) > q95 else 'inside null'}",
                  ""]

    # which door does the pulse open? (affect-03 im_end vs affect-05 ' but')
    from collections import Counter
    lines += ["## Escape channel — top-1 token at the last pulse step", ""]
    for k in ("none", "emotion", "concept", "random"):
        c = Counter(r["top5_pulse_end"][0][0]
                    for r in runs if r["kind"] == k
                    and r.get("top5_pulse_end"))
        tot = sum(c.values()) or 1
        lines.append(f"- {k}: " + ", ".join(
            f"{t!r} {n}/{tot}" for t, n in c.most_common(5)))
    esc_runs = [r for r in runs if r["escaped_in_window"]]
    if esc_runs:
        c = Counter(r["top5_pulse_end"][0][0] for r in esc_runs
                    if r.get("top5_pulse_end"))
        lines += ["", f"- among the {len(esc_runs)} in-window escapes, "
                  "top-1 at pulse end: " + ", ".join(
                      f"{t!r} {n}" for t, n in c.most_common(5))]
    lines.append("")

    (OUT / "report.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "both"
    mdl = sys.argv[2] if len(sys.argv) > 2 else "qwen-27b"
    if what in ("run", "both"):
        run(mdl)
    if what in ("analyze", "both"):
        analyze(mdl)
