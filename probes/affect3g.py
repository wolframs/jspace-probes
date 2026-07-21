"""affect-03 gemma-4b cross-check (Batch 5 of the 2026-07-21 evening
autonomous series) — does the exit-gate result (P14 falsification)
generalize across model families? bf16 + causal lens = our cleanest
instrument.

Protocol mirrors affect3.py, recalibrated for g4b:
  A  DOSE SCOUT: forced-phase TYPO amplify at MID_G4B for
     alpha_typo in SCOUT (multiples of the u6 alpha*=0.0106) —
     classify each 50-token forced phase (intact / phrase loop /
     token loop); pick a_mid (deepest non-token-loop with a loop gram)
     and a_deep (first token loop; else deepest).
  B  HYSTERESIS x FREE-PHASE CO-STEER at a_mid and a_deep:
     {none, amp-desperate, amp-calm, amp-rand1, amp-rand2} at
     alpha_e=0.12 on E_LAYERS_G4B (ws band 16-31, every 2nd).
     DVs: persists / new-loop, per-step margin, top-5 at step 0.

Emotion vectors: results/affect01-gemma-4b/vectors.pt (validated).
Qwen result being tested for generalization: calm rescues the deep
loop (exit-boost + attractor suppression), desperate blocks closure /
lowers the degeneration boundary, matched randoms null.

Output: results/affect03-g4b/{affect03g.json, report.md}
Usage:  .venv/bin/python probes/affect3g.py [run|analyze|both]
"""

import json
import re
import sys

import torch

from lab import CONFIGS, RESULTS, Steering, _strip_bos, get_model
from affect2 import _load_vectors
from affect3 import AffectSteer
from fanout import TYPO, WATER, assess
from loops import loop_gram, _null

MODEL = "gemma-4b"
MID_G4B = [15, 17, 19, 21]
E_LAYERS_G4B = [16, 18, 20, 22, 24, 26, 28, 30]
ALPHA_E = 0.12
SCOUT = [0.0106, 0.015, 0.0212, 0.03, 0.0424]
N_STEER, N_FREE = 50, 100
OUT = RESULTS / "affect03-g4b"


def _prompt_ids(lm):
    tkw = CONFIGS[MODEL].get("template_kwargs", {})
    prefix = _strip_bos(lm.tok, lm.tok.apply_chat_template(
        [{"role": "user", "content": WATER}], tokenize=False,
        add_generation_prompt=True, **tkw))
    return lm.model.encode(prefix, max_length=1_000_000)


def _gen(lm, ids, ctx, n_new):
    with ctx, torch.no_grad():
        out = lm.model._hf_model.generate(
            ids, max_new_tokens=n_new, do_sample=False,
            output_scores=True, return_dict_in_generate=True)
    text = lm.tok.decode(out.sequences[0, ids.shape[1]:],
                         skip_special_tokens=True)
    margins, top5_0 = [], None
    for i, s in enumerate(out.scores):
        vals, idxs = s[0].float().topk(5)
        margins.append(round(float(vals[0] - vals[1]), 3))
        if i == 0:
            top5_0 = [[lm.tok.decode([int(t)]), round(float(v), 2)]
                      for t, v in zip(idxs, vals)]
    return out.sequences, text, margins, top5_0


def run() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    lm = get_model(MODEL)
    V, emos = _load_vectors(MODEL)
    ids = _prompt_ids(lm)
    res = {"model": MODEL, "mid": MID_G4B, "e_layers": E_LAYERS_G4B,
           "alpha_e": ALPHA_E, "scout": []}

    def save():
        (OUT / "affect03g.json").write_text(json.dumps(res, indent=1))

    # ---- A: dose scout ------------------------------------------------
    forced = {}
    for at in SCOUT:
        with Steering(lm, TYPO, MID_G4B, "amplify", at), torch.no_grad():
            out1 = lm.model._hf_model.generate(
                ids, max_new_tokens=N_STEER, do_sample=False)
        text = lm.tok.decode(out1[0, ids.shape[1]:],
                             skip_special_tokens=True)
        g, n = loop_gram(text)
        words = re.findall(r"[A-Za-z']+", text.lower())
        token_loop = (len(set(words[-20:])) <= 2) if len(words) >= 20 \
            else False
        forced[at] = (out1, g, n, token_loop)
        res["scout"].append({"alpha_typo": at, "flags": assess(text),
                             "loop4": [g, n], "token_loop": token_loop,
                             "text": text})
        print(f"SCOUT a={at}: flags={assess(text) or 'intact'} "
              f"loop4={g!r}x{n} token_loop={token_loop} "
              f"{text[:70]!r}", flush=True)
        save()

    loopy = [a for a in SCOUT if forced[a][2] >= 3]
    deep = [a for a in SCOUT if forced[a][3]]
    a_deep = min(deep) if deep else (max(loopy) if loopy else SCOUT[-1])
    a_mid = max([a for a in loopy if a < a_deep], default=None)
    res["a_mid"], res["a_deep"] = a_mid, a_deep
    print(f"chosen: a_mid={a_mid} a_deep={a_deep}", flush=True)

    # ---- B: hysteresis grid ------------------------------------------
    conds = [("none", lambda: _null()),
             ("amp-desperate", lambda: AffectSteer(
                 lm, V, emos.index("desperate"), E_LAYERS_G4B,
                 "amplify", alpha=ALPHA_E)),
             ("amp-calm", lambda: AffectSteer(
                 lm, V, emos.index("calm"), E_LAYERS_G4B,
                 "amplify", alpha=ALPHA_E)),
             ("amp-rand1", lambda: AffectSteer(
                 lm, V, 0, E_LAYERS_G4B, "amplify", alpha=ALPHA_E,
                 rand_seed=1)),
             ("amp-rand2", lambda: AffectSteer(
                 lm, V, 0, E_LAYERS_G4B, "amplify", alpha=ALPHA_E,
                 rand_seed=2))]
    res["grid"] = []
    for at in [a for a in (a_mid, a_deep) if a is not None]:
        out1, g1, n1, _ = forced[at]
        for cname, mk in conds:
            _, cont, margins, top5_0 = _gen(lm, out1, mk(), N_FREE)
            cont_norm = " ".join(re.findall(r"[A-Za-z']+",
                                            cont.lower()))
            g2, n2 = loop_gram(cont)
            cell = {"alpha_typo": at, "cond": cname,
                    "forced_loop4": [g1, n1],
                    "persists": (bool(g1) and n1 >= 3
                                 and cont_norm.count(g1) >= 2),
                    "released_loop4": [g2, n2],
                    "released_text": cont, "margins": margins,
                    "top5_step0": top5_0}
            res["grid"].append(cell)
            print(f"  a={at} {cname:13s} persists={cell['persists']} "
                  f"loop4={g2!r}x{n2} nsteps={len(margins)} "
                  f"m0={margins[0]:.1f} mend={margins[-1]:.1f}",
                  flush=True)
            save()
    print("RUN DONE", flush=True)


def analyze() -> None:
    res = json.loads((OUT / "affect03g.json").read_text())
    lines = ["# affect-03 gemma-4b cross-check", "",
             f"MID {res['mid']}, emotion layers {res['e_layers']}, "
             f"alpha_e {res['alpha_e']}; a_mid={res.get('a_mid')} "
             f"a_deep={res.get('a_deep')}", "", "## Dose scout", ""]
    for s in res["scout"]:
        lines.append(f"- a={s['alpha_typo']}: "
                     f"{', '.join(s['flags']) or 'intact'} "
                     f"loop4={s['loop4']} token_loop={s['token_loop']}")
        lines.append(f"  - `{s['text'][:110]}`")
    lines += ["", "## Hysteresis grid", ""]
    for c in res.get("grid", []):
        m = c["margins"]
        tag = ("P" if c["persists"]
               else "NEWLOOP" if c["released_loop4"][1] >= 10
               else f"snap@{len(m)}")
        lines.append(f"- a={c['alpha_typo']} {c['cond']}: {tag}, "
                     f"loop4={c['released_loop4']}, "
                     f"m {m[0]:.1f}->{m[-1]:.1f}, "
                     f"top5(0)={c['top5_step0']}")
        lines.append(f"  - `{c['released_text'][:110]}`")
    if res.get("dose"):
        lines += ["", "## Dose-scaled ladder (a_deep, free phase)", ""]
        for c in res["dose"]:
            m = c["margins"]
            tag = ("P" if c["persists"]
                   else "NEWLOOP" if c["released_loop4"][1] >= 10
                   else f"snap@{len(m)}")
            lines.append(f"- ae={c['alpha_e']} {c['emo']}: {tag}, "
                         f"m {m[0]:.1f}->{m[-1]:.1f}, "
                         f"top5(0)={c['top5_step0']}")
    (OUT / "report.md").write_text("\n".join(lines))
    print(f"wrote {OUT / 'report.md'}", flush=True)


def dose() -> None:
    """Follow-up: alpha_e scaled to g4b's own tolerance. The first run
    showed alpha_e=0.12 is overdose everywhere on g4b (every condition
    incl. randoms destabilizes; emotion vectors install their own
    vocabulary loops). Scale by the family tolerance ratio:
    qwen ran alpha_e/alpha*_typo = 0.12/0.34 = 0.35 -> g4b analog
    ~0.0037-0.015. Grid: a_deep from the stored scout x
    {desperate, calm, rand1} x alpha_e {0.004, 0.008, 0.015, 0.03}."""
    lm = get_model(MODEL)
    V, emos = _load_vectors(MODEL)
    ids = _prompt_ids(lm)
    res = json.loads((OUT / "affect03g.json").read_text())
    a_deep = res["a_deep"]
    with Steering(lm, TYPO, MID_G4B, "amplify", a_deep), torch.no_grad():
        out1 = lm.model._hf_model.generate(
            ids, max_new_tokens=N_STEER, do_sample=False)
    g1, n1 = loop_gram(lm.tok.decode(out1[0, ids.shape[1]:],
                                     skip_special_tokens=True))
    res["dose"] = []
    for ae in (0.004, 0.008, 0.015, 0.03):
        for emo in ("desperate", "calm", "rand1"):
            if emo == "rand1":
                ctx = AffectSteer(lm, V, 0, E_LAYERS_G4B, "amplify",
                                  alpha=ae, rand_seed=1)
            else:
                ctx = AffectSteer(lm, V, emos.index(emo), E_LAYERS_G4B,
                                  "amplify", alpha=ae)
            _, cont, margins, top5_0 = _gen(lm, out1, ctx, N_FREE)
            cont_norm = " ".join(re.findall(r"[A-Za-z']+",
                                            cont.lower()))
            g2, n2 = loop_gram(cont)
            res["dose"].append({
                "alpha_typo": a_deep, "emo": emo, "alpha_e": ae,
                "persists": (bool(g1) and n1 >= 3
                             and cont_norm.count(g1) >= 2),
                "released_loop4": [g2, n2], "released_text": cont,
                "margins": margins, "top5_step0": top5_0})
            print(f"  ae={ae} {emo:9s} "
                  f"persists={res['dose'][-1]['persists']} "
                  f"loop4={g2!r}x{n2} nsteps={len(margins)} "
                  f"m0={margins[0]:.1f} mend={margins[-1]:.1f}",
                  flush=True)
            (OUT / "affect03g.json").write_text(
                json.dumps(res, indent=1))
    print("DOSE DONE", flush=True)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "both"
    if what in ("run", "both"):
        run()
    if what == "dose":
        dose()
    if what in ("analyze", "both"):
        analyze()
