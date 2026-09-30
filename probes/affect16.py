"""affect-16 — escape modes: where does the model go when a push breaks
the loop? Stop (turn-end straight out of the loop), resume (back to the
task in prose), swap (a new repeated word), or stuck.

Chunk 0 (CPU, exploratory): census over the stored affect-08 text tails.
Chunk A (GPU): exit-token ban / lift during the pulse x direction.
Prereg: results/affect16-prereg.md.
Usage:
  .venv/bin/python probes/affect16.py census
  .venv/bin/python probes/affect16.py run A
  .venv/bin/python probes/affect16.py analyze A
"""

import json
import re
import sys
from collections import Counter

import torch
from transformers import LogitsProcessor, LogitsProcessorList

from lab import RESULTS, get_model
from affect2 import _load_vectors
from affect3 import AffectSteer, E_LAYERS
from affect7 import PRE, PULSE, POST, WINDOW, TEMP, _exit_id, _prompt_ids
from affect13 import _NoCtx, _trace
from affect14 import _forced, _spearman

MODEL = "qwen-27b"
AE = 0.08
SEEDS = list(range(16, 28))
LIFT = 2.4
DIRS = ["calm", "content", "brooding", "gloomy"]

OUT = RESULTS / "affect16-q27b"
LOOP = "luckily"
MODES = ("stop", "task", "other", "swap", "stuck")
# prose exits split by content: back to the prompt's task (the water
# cycle) vs anything else (comments, meta remarks, other topics)
TASK = re.compile(r"water|cycle|evapor|condens|precipit|cloud|rain|snow|"
                  r"ocean|vapou?r|atmospher|earth|river|lake|sun")


def classify(text, exited, loop=LOOP):
    t = re.sub(r"<\|[a-z_]+\|>", " ", text)
    words = re.findall(r"[A-Za-z']+", t)
    # the tail starts mid-token; drop fragments of the loop word
    non = [w.lower() for w in words
           if w.lower() != loop and not loop.endswith(w.lower())]
    if not non:
        return "stop" if exited else "stuck"
    top, n = Counter(non).most_common(1)[0]
    if n >= 4 and n / len(non) > .5:
        return "swap"
    return "task" if TASK.search(" ".join(non)) else "other"


def census():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = {}
    for tag in ("affect08-q27b-ae08", "affect08-q27b-ae1"):
        d = json.loads((RESULTS / tag / "affect08.json").read_text())
        for r in d["runs"]:
            m = classify(r["text_tail"], r["exited"], d["loopword"])
            k = (r["cond"], r["kind"])
            e = rows.setdefault(k, {"cond": r["cond"], "kind": r["kind"],
                                    "valence": r.get("valence"),
                                    "arousal": r.get("arousal"),
                                    "n": 0, **{x: 0 for x in MODES}})
            e["n"] += 1
            e[m] += 1
    out = sorted(rows.values(), key=lambda e: (e["kind"], e["stuck"]))
    (OUT / "census-affect08.json").write_text(json.dumps(out, indent=1))
    lines = ["# affect-16 chunk 0 — escape-mode census over affect-08 "
             "(both doses pooled, 32 runs/direction)", "",
             "| cond | kind | val | aro | stop | task | other | swap | stuck |",
             "|---|---|---|---|---|---|---|---|---|"]
    for e in out:
        v = "" if e["valence"] is None else f"{e['valence']:+.2f}"
        a = "" if e["arousal"] is None else f"{e['arousal']:+.2f}"
        lines.append(f"| {e['cond']} | {e['kind']} | {v} | {a} | "
                     + " | ".join(str(e[x]) for x in MODES) + " |")
    (OUT / "census-affect08.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


class _ExitBias(LogitsProcessor):
    def __init__(self, exit_id, bias):
        self.i, self.b = exit_id, bias

    def __call__(self, input_ids, scores):
        scores[:, self.i] = (float("-inf") if self.b is None
                             else scores[:, self.i] + self.b)
        return scores


def _sample_raw(lm, ids, n, ctx=None, seed=None, proc=None):
    """affect13._sample_raw plus an optional logits processor. Raw
    logits (output_logits) are pre-processor, so traces stay raw."""
    if seed is not None:
        torch.manual_seed(seed)
    kw = {"logits_processor": LogitsProcessorList([proc])} if proc else {}
    with (ctx if ctx is not None else _NoCtx()), torch.no_grad():
        out = lm.model._hf_model.generate(
            ids, max_new_tokens=n, do_sample=True, temperature=TEMP,
            output_logits=True, return_dict_in_generate=True, **kw)
    return out.sequences, list(out.logits)


CHUNK_B = [("none", None, None), ("none_lift12", None, 1.2),
           ("brooding_lift12", "brooding", 1.2),
           ("gloomy_lift12", "gloomy", 1.2), ("sad_lift12", "sad", 1.2)] + [
    (f"{d}_ban", d, None) for d in ("reflective", "blissful", "sad",
                                    "grateful", "distressed", "hopeful")]


CHUNK_C = [("none", None, None)] + [
    (f"{d}_ban14", d, None, .14) for d in ("vigilant", "curious", "afraid",
                                           "desperate", "anxious")] + [
    (f"{d}_ban", d, None) for d in ("loving", "guilty")]


CHUNK_D = [("none", None, None)] + [
    (f"{d}_ban14", d, None, .14) for d in ("calm", "brooding", "blissful",
                                           "content", "grateful", "loving")]


def run(chunk):
    assert chunk in ("A", "B", "C", "D")
    lm = get_model(MODEL)
    ids = _prompt_ids(lm, MODEL)
    exit_id = _exit_id(lm, MODEL)
    Vemo, emos = _load_vectors(MODEL)
    forced, g1, n1, lw, loop_id = _forced(lm, ids)
    conds = []
    for d in [None] + DIRS:
        for arm, bias in (("base", False), ("ban", None), ("lift", LIFT)):
            if d is None and arm == "base":
                name = "none"
            else:
                name = f"{d or 'none'}_{arm}"
            conds.append((name, d, bias))
    if chunk != "A":
        conds = {"B": CHUNK_B, "C": CHUNK_C, "D": CHUNK_D}[chunk]
    ck = OUT / f"affect16-{chunk}.json"
    if ck.exists():
        res = json.loads(ck.read_text())
        assert res["loopword"] == lw
        done = {r["seed"] for r in res["runs"]}
        print(f"{chunk}: resuming, seeds {sorted(done)} complete", flush=True)
    else:
        res = {"model": MODEL, "alpha_e": AE, "e_layers": E_LAYERS,
               "lift": LIFT if chunk == "A" else 1.2, "forced_loop4": [g1, n1], "loopword": lw,
               "loop_id": loop_id, "exit_id": exit_id, "pre": PRE,
               "pulse": PULSE, "post": POST, "window": WINDOW,
               "conditions": [c[0] for c in conds], "seeds": SEEDS,
               "runs": []}
        done = set()
    print(f"chunk {chunk}: {len(conds)} conds x {len(SEEDS)} seeds", flush=True)
    for seed in SEEDS:
        if seed in done:
            continue
        seq1, lg1 = _sample_raw(lm, forced, PRE, seed=seed)
        if seq1.shape[1] < forced.shape[1] + PRE:
            print(f"  seed {seed}: escaped before pulse", flush=True)
            continue
        tr1 = _trace(lg1, exit_id, loop_id)
        for cond in conds:
            name, d, bias = cond[:3]
            ae = cond[3] if len(cond) > 3 else AE
            ctx = (AffectSteer(lm, Vemo, emos.index(d), E_LAYERS,
                               "amplify", ae) if d else None)
            proc = (None if bias is False or (chunk != "A" and name == "none")
                    else _ExitBias(exit_id, bias))
            seq2, lg2 = _sample_raw(lm, seq1, PULSE, ctx=ctx,
                                    seed=seed + 10_000, proc=proc)
            tr2 = _trace(lg2, exit_id, loop_id)
            if seq2.shape[1] < seq1.shape[1] + PULSE:
                seq3, tr3 = seq2, []
            else:
                seq3, lg3 = _sample_raw(lm, seq2, POST, seed=seed + 20_000)
                tr3 = _trace(lg3, exit_id, loop_id)
            n_free = seq3.shape[1] - forced.shape[1]
            exited = n_free < PRE + PULSE + POST
            text = lm.tok.decode(seq3[0, forced.shape[1]:],
                                 skip_special_tokens=False)
            res["runs"].append({
                "seed": seed, "cond": name, "n_steps": n_free,
                "exited": exited, "exit_step": n_free if exited else None,
                "mode": classify(text, exited, lw), "text": text,
                "trace": tr1 + tr2 + tr3})
            print(f"  [{chunk}] s{seed} {name:<14} {res['runs'][-1]['mode']:<6}"
                  f" exit={res['runs'][-1]['exit_step']}", flush=True)
        ck.write_text(json.dumps(res))
    print(f"chunk {chunk} DONE", flush=True)


def _analyze_b(tab):
    """R2' (lift +1.2), R4 (reroute ~ affect-14 loop drop), R5."""
    from affect14 import _deltas
    ex = lambda m: m["stop"] + m["task"] + m["other"]  # noqa: E731
    lines = []
    A = json.loads((OUT / "affect16-A.json").read_text())
    tabA = {}
    for r in A["runs"]:
        tabA.setdefault(r["cond"], Counter())[r["mode"]] += 1
    gate = tab["none_lift12"]["stuck"] >= 9
    lines.append(f"- R2' gate none+lift12 stuck "
                 f"{tab['none_lift12']['stuck']}/12 -> "
                 f"{'valid' if gate else 'UNINFORMATIVE'}")
    r2 = []
    for d in ("brooding", "gloomy"):
        b, l_ = tabA[f"{d}_base"], tab[f"{d}_lift12"]
        pb = (b["task"] + b["other"]) / ex(b) if ex(b) else 0
        pl = (l_["task"] + l_["other"]) / ex(l_) if ex(l_) else 0
        r2.append(pl <= pb / 2)
        lines.append(f"- R2' {d}: prose share of exits base {pb:.2f} -> "
                     f"lift12 {pl:.2f} (exits {ex(l_)}) -> "
                     f"{'PASS' if r2[-1] else 'FAIL'}")
    s_ = tab["sad_lift12"]
    lines.append(f"- sad lift12 (descriptive): stop {s_['stop']}, prose "
                 f"{s_['task'] + s_['other']}, stuck {s_['stuck']}")
    lines.append(f"- **R2': {'PASS' if all(r2) and gate else 'FAIL' if gate else 'UNINFORMATIVE'}**")
    p1 = json.loads((RESULTS / "affect14-q27b" /
                     "affect14-part1.json").read_text())
    dd = _deltas(p1)
    cen = {e["cond"]: e for e in json.loads(
        (OUT / "census-affect08.json").read_text())}
    pts = []
    for t_, src in ((tabA, "A"), (tab, "B")):
        for c, m in t_.items():
            if c.endswith("_ban") and c != "none_ban":
                d = c[:-4]
                pts.append((d, m["task"] + m["other"] + m["swap"],
                            -dd[d][1], cen[d]["arousal"], src))
    pts.sort(key=lambda x: -x[1])
    lines += ["", "| direction | ban reroutes /12 | affect-14 −dLoop | "
              "arousal | chunk |", "|---|---|---|---|---|"]
    lines += [f"| {d} | {n} | {l:.2f} | {a:+.0f} | {s} |"
              for d, n, l, a, s in pts]
    rho = _spearman([p[2] for p in pts], [p[1] for p in pts])
    rho_a = _spearman([p[3] for p in pts], [p[1] for p in pts])
    lines += ["", f"- **R4** Spearman(reroutes, −dLoop) = {rho:+.3f} "
              f"(bar .5) -> {'PASS' if rho >= .5 else 'FAIL'}; vs arousal "
              f"{rho_a:+.3f} (n={len(pts)})"]
    return lines


def _first_step(res):
    """{cond: mean first-pulse-step (dExit, dLoop)} vs none, per seed."""
    pre = res["pre"]
    none = {r["seed"]: r["trace"][pre] for r in res["runs"]
            if r["cond"] == "none"}
    acc = {}
    for r in res["runs"]:
        if r["cond"] != "none" and len(r["trace"]) > pre:
            n = none[r["seed"]]
            acc.setdefault(r["cond"], []).append(
                (r["trace"][pre][0] - n[0], r["trace"][pre][1] - n[1]))
    return {c: (sum(x[0] for x in v) / len(v), sum(x[1] for x in v) / len(v))
            for c, v in acc.items()}


def _analyze_c():
    cen = {e["cond"]: e for e in json.loads(
        (OUT / "census-affect08.json").read_text())}
    pts, swaps = [], {}
    for ch in ("A", "B", "C"):
        res = json.loads((OUT / f"affect16-{ch}.json").read_text())
        fs = _first_step(res)
        tab = {}
        for r in res["runs"]:
            tab.setdefault(r["cond"], Counter())[r["mode"]] += 1
            if r["mode"] == "swap":
                w = [x.lower() for x in re.findall(r"[A-Za-z']+", r["text"])
                     if x.lower() != res["loopword"]]
                swaps.setdefault(r["cond"], Counter()).update(
                    [Counter(w).most_common(1)[0][0]])
        for c, m in tab.items():
            if "_ban" in c and not c.startswith("none"):
                d = c.split("_ban")[0]
                pts.append((c, m["task"] + m["other"] + m["swap"],
                            -fs[c][1], cen[d]["arousal"], ch))
    pts.sort(key=lambda x: -x[2])
    lines = ["", "| ban arm | reroutes /12 | first-step −dLoop | arousal "
             "| chunk |", "|---|---|---|---|---|"]
    lines += [f"| {c} | {n} | {l:.2f} | {a:+.0f} | {ch} |"
              for c, n, l, a, ch in pts]
    rho = _spearman([p[2] for p in pts], [p[1] for p in pts])
    lines += ["", f"- **R6** Spearman(reroutes, first-step −dLoop) = "
              f"{rho:+.3f} (n={len(pts)}, bar .5) -> "
              f"{'PASS' if rho >= .5 else 'FAIL'}"]
    med = sorted(p[2] for p in pts)[len(pts) // 2]
    hi = [p[1] for p in pts if p[2] > med and p[3] > 0]
    lo = [p[1] for p in pts if p[2] > med and p[3] < 0]
    if not hi:
        v = "UNTESTABLE"
    else:
        mh, ml = sum(hi) / len(hi), (sum(lo) / len(lo) if lo else 0)
        v = "PASS" if mh >= ml / 2 else "FAIL"
    lines.append(f"- **R7** above-median push (median {med:.2f}): "
                 f"high-arousal reroutes {hi}, low-arousal {lo} -> {v}")
    lines.append("- swap fillers: " + "; ".join(
        f"{c}: {dict(v)}" for c, v in swaps.items()))
    return lines


def _leak(tab, arms):
    rer = sum(tab[a]["task"] + tab[a]["other"] + tab[a]["swap"]
              for a in arms)
    leak = sum(tab[a]["other"] + tab[a]["swap"] for a in arms)
    return leak, rer


def _analyze_d(tab):
    C = json.loads((OUT / "affect16-C.json").read_text())
    tabC = {}
    for r in C["runs"]:
        tabC.setdefault(r["cond"], Counter())[r["mode"]] += 1
    lc, rc = _leak(tabC, [c for c in tabC if c.endswith("_ban14")])
    arms = [c for c in tab if c.endswith("_ban14")]
    ld, rd = _leak(tab, arms)
    sc, sd = lc / rc, (ld / rd if rd else 0.0)
    return ["", f"- C high-arousal α .14: leak {lc}/{rc} reroutes = "
            f"{sc:.3f}; bar = {sc / 2:.3f}",
            f"- **R8** D low-arousal α .14: leak {ld}/{rd} reroutes = "
            f"{sd:.3f} -> {'PASS' if rd and sd >= sc / 2 else 'FAIL'}"]


def analyze(chunk):
    res = json.loads((OUT / f"affect16-{chunk}.json").read_text())
    pre, pulse = res["pre"], res["pulse"]
    none = {r["seed"]: r["trace"] for r in res["runs"]
            if r["cond"] == "none"}
    tab, dl = {}, {}
    for r in res["runs"]:
        tab.setdefault(r["cond"], Counter())[r["mode"]] += 1
        nt = none[r["seed"]]
        k = range(pre, min(pre + pulse, len(r["trace"]), len(nt)))
        if r["cond"] != "none" and k:
            dl.setdefault(r["cond"], []).append((
                sum(r["trace"][t][0] - nt[t][0] for t in k) / len(k),
                sum(r["trace"][t][1] - nt[t][1] for t in k) / len(k)))
    lines = [f"# affect-16 chunk {chunk} — exit ban / lift x direction "
             f"(qwen-27b, {len(res['seeds'])} seeds, lift +{res['lift']})",
             "", "| cond | stop | task | other | swap | stuck | "
             "raw dExit | raw dLoop | stop steps |",
             "|---|---|---|---|---|---|---|---|---|"]
    for c in res["conditions"]:
        m = tab[c]
        de = (f"{sum(x[0] for x in dl[c]) / len(dl[c]):+.2f}"
              if c in dl else "—")
        dlp = (f"{sum(x[1] for x in dl[c]) / len(dl[c]):+.2f}"
               if c in dl else "—")
        steps = sorted(r["exit_step"] for r in res["runs"]
                       if r["cond"] == c and r["mode"] == "stop")
        lines.append(f"| {c} | " + " | ".join(str(m[x]) for x in MODES)
                     + f" | {de} | {dlp} | {steps} |")
    ex = lambda m: m["stop"] + m["task"] + m["other"]  # noqa: E731
    if chunk == "A":
        lines.append("")
        r1 = []
        for d in ("calm", "content"):
            b, n = tab[f"{d}_base"], tab[f"{d}_ban"]
            out = n["task"] + n["other"] + n["swap"]
            ok = out >= .5 * (ex(b) + b["swap"])
            r1.append(ok)
            lines.append(f"- R1 {d}: base exits {ex(b) + b['swap']}, ban "
                         f"reroutes {out} (task {n['task']}, other "
                         f"{n['other']}, swap {n['swap']}), delayed stops "
                         f"{n['stop']}, stuck {n['stuck']} -> "
                         f"{'PASS' if ok else 'FAIL'}")
        lines.append(f"- **R1: {'PASS' if all(r1) else 'FAIL'}**")
        gate = tab["none_lift"]["stuck"] >= 9
        lines.append(f"- R2 gate none+lift stuck {tab['none_lift']['stuck']}/12"
                     f" -> {'valid' if gate else 'UNINFORMATIVE'}")
        r2 = []
        for d in ("brooding", "gloomy"):
            b, l_ = tab[f"{d}_base"], tab[f"{d}_lift"]
            pb = (b["task"] + b["other"]) / ex(b) if ex(b) else 0
            pl = (l_["task"] + l_["other"]) / ex(l_) if ex(l_) else 0
            ok = pl <= pb / 2
            r2.append(ok)
            lines.append(f"- R2 {d}: prose share of exits base {pb:.2f} -> "
                         f"lift {pl:.2f} -> {'PASS' if ok else 'FAIL'}")
        lines.append(f"- **R2: {'PASS' if all(r2) and gate else 'FAIL' if gate else 'UNINFORMATIVE'}**")
    elif chunk == "B":
        lines += _analyze_b(tab)
    elif chunk == "C":
        lines += _analyze_c()
    else:
        lines += _analyze_d(tab)
    lines += ["", "## ban-arm prose (first 3 per direction)", ""]
    for c in [c for c in res["conditions"]
              if "_ban" in c and not c.startswith("none")]:
        for r in [r for r in res["runs"] if r["cond"] == c
                  and r["mode"] in ("other", "swap", "task")][:3]:
            d = c
            t = r["text"].replace(res["loopword"], "").strip()
            lines.append(f"- {d} s{r['seed']} {r['mode']}: "
                         f"`{' '.join(t.split())[:160]}`")
    (OUT / f"report-{chunk}.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    what = sys.argv[1]
    if what == "census":
        census()
    elif what == "run":
        run(sys.argv[2])
    else:
        analyze(sys.argv[2])
